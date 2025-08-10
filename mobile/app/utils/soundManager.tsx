// utils/soundManager.ts
import { Audio } from "expo-av";

class SoundManager {
  // --- State ---
  private static carpetSound: Audio.Sound | null = null;
  private static carpetAssetId: number | null = null; // require(...) numeric id
  private static currentCarpetKey: string | null = null; // logical key, e.g. "windy_mountains.mp3"

  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading = false;
  private static swapToken = 0; // cancels older swaps so web doesn't throw DOMException

  // --- Small helpers ---
  private static now = () =>
    typeof performance !== "undefined" ? performance.now() : Date.now();
  private static sleep(ms: number) {
    return new Promise((r) => setTimeout(r, ms));
  }

  // Equal‑power easing (perceived‑loudness friendly)
  private static equalPowerIn(t: number) {
    // t in [0,1] for fade‑in
    return Math.sin((Math.PI / 2) * t);
  }
  private static equalPowerOut(t: number) {
    // t in [0,1] for fade‑out
    return Math.cos((Math.PI / 2) * t);
  }

  /** Crossfade: fade new in & old out with equal‑power curve (overlap). */
  private static async crossFade(
    oldSound: Audio.Sound | null,
    newSound: Audio.Sound,
    durationMs = 900,
    newTargetVol = 0.6
  ) {
    try {
      await newSound.setStatusAsync({
        volume: 0,
        shouldPlay: true,
        isLooping: true,
      });
    } catch {}
    const start = this.now();
    let t = 0;

    // ~60fps loop
    while (t < 1) {
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / durationMs);

      const vIn = this.equalPowerIn(t) * newTargetVol; // 0→target
      const vOut = this.equalPowerOut(t); // 1→0

      try {
        await newSound.setStatusAsync({ volume: vIn });
      } catch {}
      if (oldSound) {
        try {
          await oldSound.setStatusAsync({ volume: vOut });
        } catch {}
      }
      await this.sleep(16);
    }
  }

  /** (Optional) vanilla fades kept for triggers */
  private static async fadeIn(
    sound: Audio.Sound,
    duration = 300,
    targetVolume = 0.8
  ) {
    const start = this.now();
    let t = 0;
    try {
      await sound.setStatusAsync({ volume: 0 });
    } catch {}
    while (t < 1) {
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / duration);
      const v = this.equalPowerIn(t) * targetVolume;
      try {
        await sound.setStatusAsync({ volume: v });
      } catch {}
      await this.sleep(16);
    }
  }

  // -------- Public API --------

  /**
   * Start/swap ambience with smooth crossfade.
   * 2nd arg can be:
   *  - string (ambience key): prevents reloading if same
   *  - number (fadeMs): set fade duration
   *
   * Usage:
   *   playCarpet(SOUND_MAP[key], key)
   *   playCarpet(SOUND_MAP[key], 1000) // if you don't track keys
   */
  static async playCarpet(
    asset: number,
    keyOrFade?: string | number,
    fadeMs = 900
  ) {
    // Parse flexible arg
    let key: string | undefined;
    if (typeof keyOrFade === "string") key = keyOrFade;
    else if (typeof keyOrFade === "number") fadeMs = keyOrFade;

    // Skip if same ambience already playing
    if (key && this.currentCarpetKey === key && this.carpetSound) return;
    if (!key && this.carpetAssetId === asset && this.carpetSound) return;

    if (this.isCarpetLoading) return;
    const myToken = ++this.swapToken;
    this.isCarpetLoading = true;

    // Preload "next"
    let next: Audio.Sound | null = null;
    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: true,
        volume: 0, // start silent; crossFade will ramp
      });
      next = sound;
    } catch (e) {
      console.warn("[SoundManager] Carpet load error:", e);
      this.isCarpetLoading = false;
      return;
    }

    // Another swap started meanwhile? discard this one cleanly
    if (myToken !== this.swapToken) {
      try {
        await next.unloadAsync();
      } catch {}
      this.isCarpetLoading = false;
      return;
    }

    // Equal‑power crossfade overlap
    await this.crossFade(this.carpetSound, next, fadeMs, 0.6).catch(() => {});

    // Unload old AFTER overlap completes (avoids audible gap)
    if (this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
      } catch {}
      try {
        await this.carpetSound.unloadAsync();
      } catch {}
    }

    // Commit new state
    this.carpetSound = next;
    this.carpetAssetId = asset;
    if (key) this.currentCarpetKey = key;
    this.isCarpetLoading = false;

    console.log("🎵 Carpet swapped (equal‑power crossfade)");
  }

  /** Fade out & stop ambience smoothly. */
  static async stopCarpet(fadeMs = 600) {
    this.swapToken++; // cancel in‑flight swaps
    const old = this.carpetSound;
    this.carpetSound = null;
    this.carpetAssetId = null;
    this.currentCarpetKey = null;
    if (!old) return;

    // Equal‑power fade‑out
    const start = this.now();
    let t = 0;
    while (t < 1) {
      const elapsed = this.now() - start;
      t = Math.min(1, elapsed / fadeMs);
      const vOut = this.equalPowerOut(t);
      try {
        await old.setStatusAsync({ volume: vOut });
      } catch {}
      await this.sleep(16);
    }
    try {
      await old.stopAsync();
    } catch {}
    try {
      await old.unloadAsync();
    } catch {}

    console.log("🛑 Carpet stopped (smooth fade out)");
  }

  /** Hard stop everything (ambience + all one‑shots). */
  static async stopAll() {
    this.swapToken++; // cancel swaps
    await this.stopCarpet(0);

    for (const s of [...this.activeSounds]) {
      try {
        await s.stopAsync();
      } catch {}
      try {
        await s.unloadAsync();
      } catch {}
      this.activeSounds.delete(s);
    }
    console.log("✅ All sounds stopped");
  }

  /**
   * Play a one‑shot SFX (trigger).
   * Resolves when playback ends, so UI can clear highlights with `.finally()`.
   */
  static async playTrigger(asset: number): Promise<void> {
    let sound: Audio.Sound | null = null;
    try {
      const created = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: false,
        volume: 0,
      });
      sound = created.sound;
      this.activeSounds.add(sound);

      await this.fadeIn(sound, 300, 0.8);

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
      console.warn("[SoundManager] Trigger play error:", e);
      if (sound) {
        try {
          await sound.unloadAsync();
        } catch {}
        this.activeSounds.delete(sound);
      }
      // Resolve anyway so UI logic doesn't hang
      return;
    }
  }
}

export default SoundManager;
