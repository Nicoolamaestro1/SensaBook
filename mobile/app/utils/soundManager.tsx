// utils/soundManager.ts
import { Audio } from "expo-av";
import { Platform } from "react-native";

class SoundManager {
  // --- State ---
  private static carpetSound: Audio.Sound | null = null;
  private static carpetAssetId: number | null = null;
  private static currentCarpetKey: string | null = null;

  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading = false;

  /** Global swap token (ambience + global aborts). */
  private static swapToken = 0;

  /** Trigger-only token: bump this to abort/retire trigger fades & playback. */
  private static triggerSwapToken = 0;

  private static audioModeReady = false;

  // --- Helpers ---
  private static now = () =>
    typeof performance !== "undefined" ? performance.now() : Date.now();
  private static sleep(ms: number) {
    return new Promise((r) => setTimeout(r, ms));
  }

  // --- Volumes (defaults) ---
  private static carpetVolume = 0.6; // 0..1
  private static triggerVolume = 0.8; // 0..1

  /** Set ambience (carpet) volume, 0..1. Applies immediately if playing. */
  static async setCarpetVolume(v: number) {
    this.carpetVolume = Math.max(0, Math.min(1, v));
    if (this.carpetSound) {
      try {
        await this.carpetSound.setVolumeAsync(this.carpetVolume);
      } catch {}
    }
  }

  /** Set trigger one-shots volume, 0..1. Will be used for future triggers. */
  static setTriggerVolume(v: number) {
    this.triggerVolume = Math.max(0, Math.min(1, v));
  }

  private static async ensureAudioMode() {
    if (this.audioModeReady) return;

    try {
      const opts: any = {
        staysActiveInBackground: false,
      };

      if (Platform.OS === "ios") {
        opts.playsInSilentModeIOS = true;
        const iEnum = (Audio as any).InterruptionModeIOS;
        opts.interruptionModeIOS =
          iEnum?.MixWithOthers ??
          (Audio as any).INTERRUPTION_MODE_IOS_MIX_WITH_OTHERS;
      } else if (Platform.OS === "android") {
        opts.shouldDuckAndroid = false;
        opts.playThroughEarpieceAndroid = false;
        const aEnum = (Audio as any).InterruptionModeAndroid;
        opts.interruptionModeAndroid =
          aEnum?.DoNotMix ??
          (Audio as any).INTERRUPTION_MODE_ANDROID_DO_NOT_MIX;
      } else {
        // web: set nothing extra
      }

      await Audio.setAudioModeAsync(opts);
    } catch (e) {
      console.warn("[SoundManager] setAudioMode failed (non-fatal):", e);
    } finally {
      this.audioModeReady = true;
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

    let lastOld = oldStartVol;
    let lastNew = newStartVol;

    const start = this.now();
    let t = 0;

    while (t < 1) {
      if (myToken !== this.swapToken) return; // aborted globally

      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / durationMs);

      const targetIn = this.equalPowerIn(t) * newTargetVol;
      const targetOut = this.equalPowerOut(t) * oldStartVol;

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

      await this.sleep(16);
    }
  }

  /** Abortable equal-power fade-in (never-down clamp). */
  private static async fadeIn(
    sound: Audio.Sound,
    duration = 300,
    targetVolume = 0.8,
    globalToken?: number,
    triggerToken?: number
  ) {
    const s0 = await sound.getStatusAsync().catch(() => null as any);
    let last =
      s0 && s0.isLoaded && typeof s0.volume === "number" ? s0.volume : 0;

    const start = this.now();
    let t = 0;

    while (t < 1) {
      // abort if either token changed
      if (
        (globalToken != null && globalToken !== this.swapToken) ||
        (triggerToken != null && triggerToken !== this.triggerSwapToken)
      ) {
        break;
      }

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

  /** Equal-power fade-out to 0 (never-up clamp). */
  private static async fadeOut(
    sound: Audio.Sound,
    duration = 250
  ): Promise<void> {
    let s0: any = null;
    try {
      s0 = await sound.getStatusAsync();
    } catch {}
    const startVol =
      s0 && s0.isLoaded && typeof s0.volume === "number" ? s0.volume : 0;

    let last = startVol;
    const start = this.now();
    let t = 0;

    while (t < 1) {
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / Math.max(1, duration));
      const target = this.equalPowerOut(t) * startVol; // startVol -> 0
      const next = Math.min(last, target); // never-up
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

    console.log(`🎵 Ambient carpet requested: "${key}"`);
    if (key && this.currentCarpetKey === key && this.carpetSound) return;
    if (!key && this.carpetAssetId === asset && this.carpetSound) return;

    if (this.isCarpetLoading) return;
    const myToken = ++this.swapToken;
    this.isCarpetLoading = true;

    let next: Audio.Sound | null = null;
    try {
      const created = await Audio.Sound.createAsync(asset, {
        shouldPlay: false,
        isLooping: true,
        volume: 0.0,
      });
      next = created.sound;
      await next.setVolumeAsync(0.0);
      await this.sleep(10);
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

    await this.crossFade(
      this.carpetSound,
      next,
      fadeMs,
      this.carpetVolume,
      myToken
    ).catch(() => {});

    if (myToken === this.swapToken && this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
      } catch {}
      try {
        await this.carpetSound.unloadAsync();
      } catch {}
    }

    if (myToken === this.swapToken) {
      this.carpetSound = next;
      this.carpetAssetId = asset;
      if (key) this.currentCarpetKey = key;
    } else {
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

    // Fade out from current volume
    let s0: any = null;
    try {
      s0 = await old.getStatusAsync();
    } catch {}
    const startVol =
      s0 && s0.isLoaded && typeof s0.volume === "number" ? s0.volume : 0;

    let last = startVol;
    const start = this.now();
    let t = 0;
    while (t < 1) {
      if (myToken !== this.swapToken) break; // another stop started
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / Math.max(1, fadeMs));
      const target = this.equalPowerOut(t) * startVol; // startVol -> 0
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

  /** Fade out ONLY one-shot trigger sounds (used on screen blur/unmount). */
  static async stopTriggers(fadeMs = 250) {
    // Signal new generation for triggers so any in-flight trigger fade-ins stop rising
    this.triggerSwapToken++;

    const sounds = [...this.activeSounds];
    await Promise.all(
      sounds.map(async (s) => {
        try {
          // detach status updates to avoid double-calls during manual stop
          try {
            s.setOnPlaybackStatusUpdate(null);
          } catch {}
          await this.fadeOut(s, fadeMs);
          try {
            await s.stopAsync();
          } catch {}
          try {
            await s.unloadAsync();
          } catch {}
        } finally {
          this.activeSounds.delete(s);
        }
      })
    );
  }

  /** Hard stop everything (ambience + one-shots). Aborts all fades. */
  static async stopAll() {
    const myToken = ++this.swapToken; // abort everything (global)
    this.triggerSwapToken++; // also abort any trigger fades
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

    // Fade out triggers quickly for a cleaner stop
    await this.stopTriggers(150);
  }

  /** Play a one-shot trigger. */
  static async playTrigger(asset: number): Promise<void> {
    await this.ensureAudioMode();

    const globalToken = this.swapToken;
    const triggerToken = this.triggerSwapToken;

    let sound: Audio.Sound | null = null;
    try {
      // Start muted, then play and fade-in (abortable by tokens)
      const created = await Audio.Sound.createAsync(asset, {
        shouldPlay: false,
        isLooping: false,
        volume: 0.0,
      });
      sound = created.sound;
      this.activeSounds.add(sound);

      try {
        await sound.setVolumeAsync(0.0);
      } catch {}
      await this.sleep(10);
      try {
        await sound.playAsync();
      } catch {}

      await this.fadeIn(
        sound,
        250,
        this.triggerVolume,
        globalToken,
        triggerToken
      );

      return new Promise<void>((resolve) => {
        sound!.setOnPlaybackStatusUpdate((status: any) => {
          if (!status || !status.isLoaded) return;

          // If trigger generation changed (e.g., stopTriggers called), we bail here.
          if (triggerToken !== this.triggerSwapToken) {
            try {
              sound!.setOnPlaybackStatusUpdate(null);
            } catch {}
            // stopTriggers() will do the fade & unload; we just resolve.
            resolve();
            return;
          }

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
