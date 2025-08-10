// utils/soundManager.ts
import { Audio } from "expo-av";

class SoundManager {
  // --- State ---
  private static carpetSound: Audio.Sound | null = null;
  private static carpetAssetId: number | null = null;
  private static currentCarpetKey: string | null = null;

  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading = false;

  /** Increments whenever we start/stop/cancel. Any async work should
   *  check this value and bail if it changes. */
  private static swapToken = 0;
  private static audioModeReady = false;

  // --- Helpers ---
  private static now = () =>
    typeof performance !== "undefined" ? performance.now() : Date.now();
  private static sleep(ms: number) {
    return new Promise((r) => setTimeout(r, ms));
  }

  private static async ensureAudioMode() {
    if (this.audioModeReady) return;
    try {
      await Audio.setAudioModeAsync({
        playsInSilentModeIOS: true,
        interruptionModeIOS: Audio.INTERRUPTION_MODE_IOS_MIX_WITH_OTHERS,
        allowsRecordingIOS: false,
        shouldDuckAndroid: false,
        interruptionModeAndroid: Audio.INTERRUPTION_MODE_ANDROID_DO_NOT_MIX,
        playThroughEarpieceAndroid: false,
        staysActiveInBackground: false,
      });
      this.audioModeReady = true;
    } catch (e) {
      console.warn("[SoundManager] setAudioMode failed:", e);
    }
  }

  private static equalPowerIn(t: number) {
    return Math.sin((Math.PI / 2) * t);
  }
  private static equalPowerOut(t: number) {
    return Math.cos((Math.PI / 2) * t);
  }

  /** Abortable equal-power crossfade with "never-up" clamps. */
  private static async crossFade(
    oldSound: Audio.Sound | null,
    newSound: Audio.Sound,
    durationMs: number,
    newTargetVol: number,
    myToken: number
  ) {
    // Capture starting volumes once
    let oldStartVol = 0;
    if (oldSound) {
      try {
        const s = await oldSound.getStatusAsync();
        if (s.isLoaded && typeof s.volume === "number") oldStartVol = s.volume;
      } catch {}
    }

    let newStartVol = 0;
    try {
      const s2 = await newSound.getStatusAsync();
      if (s2.isLoaded && typeof s2.volume === "number") newStartVol = s2.volume;
    } catch {}

    // Monotonic volumes we actually apply (never increase old, never decrease new)
    let lastOld = oldStartVol;
    let lastNew = newStartVol;

    const start = this.now();
    let t = 0;

    while (t < 1) {
      // Abort if someone called stopCarpet/stopAll or another swap started
      if (myToken !== this.swapToken) return;

      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / durationMs);

      const targetIn = this.equalPowerIn(t) * newTargetVol; // 0 → target
      const targetOut = this.equalPowerOut(t) * oldStartVol; // oldStart → 0

      // Never-up clamps
      const nextNew = Math.max(lastNew, targetIn);
      const nextOld = Math.min(lastOld, targetOut);

      try {
        await newSound.setVolumeAsync(nextNew);
      } catch {}
      if (oldSound) {
        try {
          await oldSound.setVolumeAsync(nextOld);
        } catch {}
      }

      lastNew = nextNew;
      lastOld = nextOld;

      await this.sleep(16); // ~60fps
    }
  }

  /** Quick fade-in for one-shots (never-down clamp). */
  private static async fadeIn(
    sound: Audio.Sound,
    duration = 300,
    targetVolume = 0.8
  ) {
    const s0 = await sound.getStatusAsync().catch(() => null as any);
    let last =
      s0 && s0.isLoaded && typeof s0.volume === "number" ? s0.volume : 0;
    const start = this.now();
    let t = 0;
    while (t < 1) {
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / duration);
      const target = this.equalPowerIn(t) * targetVolume;
      const next = Math.max(last, target);
      try {
        await sound.setVolumeAsync(next);
      } catch {}
      last = next;
      await this.sleep(16);
    }
  }

  // -------- Public API --------

  /** Start/swap ambience with smooth, abortable crossfade. */
  static async playCarpet(
    asset: number,
    keyOrFade?: string | number,
    fadeMs = 900
  ) {
    await this.ensureAudioMode();

    let key: string | undefined;
    if (typeof keyOrFade === "string") key = keyOrFade;
    else if (typeof keyOrFade === "number") fadeMs = keyOrFade;

    // Skip if same ambience already playing
    if (key && this.currentCarpetKey === key && this.carpetSound) return;
    if (!key && this.carpetAssetId === asset && this.carpetSound) return;

    // Prevent concurrent loads
    if (this.isCarpetLoading) return;
    const myToken = ++this.swapToken;
    this.isCarpetLoading = true;

    // Create the next sound fully muted and paused
    let next: Audio.Sound | null = null;
    try {
      const created = await Audio.Sound.createAsync(asset, {
        shouldPlay: false,
        isLooping: true,
        volume: 0.0,
      });
      next = created.sound;
      await next.setVolumeAsync(0.0);
      await this.sleep(10); // ensure native applies volume 0
      if (myToken !== this.swapToken) {
        await next.unloadAsync().catch(() => {});
        this.isCarpetLoading = false;
        return;
      }
      await next.playAsync(); // start silent
    } catch (e) {
      console.warn("[SoundManager] Carpet load error:", e);
      this.isCarpetLoading = false;
      return;
    }

    if (myToken !== this.swapToken) {
      await next.unloadAsync().catch(() => {});
      this.isCarpetLoading = false;
      return;
    }

    // Crossfade with "never-up" clamps and abort checks
    await this.crossFade(this.carpetSound, next, fadeMs, 0.6, myToken).catch(
      () => {}
    );

    // After fade completes (and not aborted), unload old
    if (myToken === this.swapToken && this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
      } catch {}
      try {
        await this.carpetSound.unloadAsync();
      } catch {}
    }

    // Commit new state if still current
    if (myToken === this.swapToken) {
      this.carpetSound = next;
      this.carpetAssetId = asset;
      if (key) this.currentCarpetKey = key;
    } else {
      // We were aborted: unload the "next" we created
      await next.unloadAsync().catch(() => {});
    }

    this.isCarpetLoading = false;
  }

  /** Fade out & stop ambience smoothly. Aborts any running crossfade. */
  static async stopCarpet(fadeMs = 600) {
    const myToken = ++this.swapToken; // abort in-flight crossfades
    const old = this.carpetSound;

    this.carpetSound = null;
    this.carpetAssetId = null;
    this.currentCarpetKey = null;

    if (!old) return;

    // Fade out from whatever volume it has now; monotonic down
    let s0: any = null;
    try {
      s0 = await old.getStatusAsync();
    } catch {}
    let last =
      s0 && s0.isLoaded && typeof s0.volume === "number" ? s0.volume : 0;

    const start = this.now();
    let t = 0;
    while (t < 1) {
      if (myToken !== this.swapToken) break; // another stop started
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / Math.max(1, fadeMs));
      const target = this.equalPowerOut(t) * last; // startVol -> 0
      const next = Math.min(last, target); // never-up
      try {
        await old.setVolumeAsync(next);
      } catch {}
      last = next;
      await this.sleep(16);
    }

    try {
      await old.stopAsync();
    } catch {}
    try {
      await old.unloadAsync();
    } catch {}
  }

  /** Hard stop everything (ambience + one-shots). Aborts all fades. */
  static async stopAll() {
    const myToken = ++this.swapToken; // abort everything
    this.isCarpetLoading = false;

    // Stop ambience immediately
    const old = this.carpetSound;
    this.carpetSound = null;
    this.carpetAssetId = null;
    this.currentCarpetKey = null;

    if (old) {
      try {
        await old.stopAsync();
      } catch {}
      try {
        await old.unloadAsync();
      } catch {}
    }

    // Stop any one-shots
    for (const s of [...this.activeSounds]) {
      try {
        await s.stopAsync();
      } catch {}
      try {
        await s.unloadAsync();
      } catch {}
      this.activeSounds.delete(s);
    }
  }

  /** Play a one-shot trigger. */
  static async playTrigger(asset: number): Promise<void> {
    await this.ensureAudioMode();

    let sound: Audio.Sound | null = null;
    try {
      const created = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: false,
        volume: 0.0,
      });
      sound = created.sound;
      this.activeSounds.add(sound);

      await this.fadeIn(sound, 250, 0.8);

      return new Promise<void>((resolve) => {
        sound!.setOnPlaybackStatusUpdate((status: any) => {
          if (!status || !status.isLoaded) return;
          if (
            status.didJustFinish ||
            (!status.isPlaying && status.positionMillis > 0)
          ) {
            try {
              sound!.setOnPlaybackStatusUpdate(null);
            } catch {}
            sound!.unloadAsync().catch(() => {});
            this.activeSounds.delete(sound!);
            resolve();
          }
        });
      });
    } catch (e) {
      if (sound) {
        try {
          await sound.unloadAsync();
        } catch {}
        this.activeSounds.delete(sound);
      }
      return;
    }
  }
}

export default SoundManager;
