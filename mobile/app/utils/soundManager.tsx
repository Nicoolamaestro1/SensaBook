import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static carpetAssetKey: any = null;
  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading: boolean = false;
  private static swapToken = 0; // cancels in-flight swaps

  // Smooth fade-in
  static async fadeIn(sound: Audio.Sound, duration = 1200, targetVolume = 0.5) {
    const steps = 10;
    const stepTime = duration / steps;
    await sound.setVolumeAsync(0.02);
    for (let i = 1; i <= steps; i++) {
      await sound.setVolumeAsync((i / steps) * targetVolume);
      await new Promise((res) => setTimeout(res, stepTime));
    }
  }

  // Smooth fade-out
  static async fadeOut(sound: Audio.Sound, duration = 800) {
    const status = await sound.getStatusAsync();
    if (!status.isLoaded) return;
    const initialVolume = status.volume ?? 1.0;
    const steps = 10;
    const stepTime = duration / steps;
    for (let i = steps - 1; i >= 0; i--) {
      await sound.setVolumeAsync((i / steps) * initialVolume);
      await new Promise((res) => setTimeout(res, stepTime));
    }
    await sound.stopAsync();
    await sound.unloadAsync();
  }

  // Stops all active sounds
  static async stopAll() {
    this.swapToken++; // cancel pending swaps
    await this.stopCarpet();
    for (const sound of this.activeSounds) {
      try {
        await sound.stopAsync();
        await sound.unloadAsync();
      } catch {}
    }
    this.activeSounds.clear();
    console.log("✅ All sounds stopped");
  }

  /**
   * Cross-fade to new carpet (safe on web).
   * Call this instead of stop+play.
   */
  static async playCarpet(asset: any, fadeMs = 800) {
    if (this.isCarpetLoading) return;
    if (this.carpetAssetKey === asset && this.carpetSound) return; // already playing same

    const myToken = ++this.swapToken;
    this.isCarpetLoading = true;

    let next: Audio.Sound | null = null;
    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: true,
        volume: 0.02,
      });
      next = sound;
    } catch (e) {
      console.log("Carpet load error:", e);
      this.isCarpetLoading = false;
      return;
    }

    if (myToken !== this.swapToken) {
      try {
        await next.unloadAsync();
      } catch {}
      this.isCarpetLoading = false;
      return;
    }

    await Promise.all([
      this.fadeIn(next, fadeMs, 0.5),
      this.fadeOut(this.carpetSound, fadeMs),
    ]).catch(() => {});

    if (this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
      } catch {}
      try {
        await this.carpetSound.unloadAsync();
      } catch {}
    }

    this.carpetSound = next;
    this.carpetAssetKey = asset;
    this.isCarpetLoading = false;
    console.log("🎵 Carpet sound swapped (crossfade)");
  }

  // Fade-out and stop current carpet
  static async stopCarpet(fadeMs = 800) {
    this.swapToken++;
    if (this.carpetSound) {
      try {
        await this.fadeOut(this.carpetSound, fadeMs);
        console.log("🛑 Carpet sound stopped (with fade out)");
      } catch {
        try {
          await this.carpetSound.stopAsync();
        } catch {}
        try {
          await this.carpetSound.unloadAsync();
        } catch {}
      }
      this.carpetSound = null;
      this.carpetAssetKey = null;
    }
  }

  /**
   * Plays a one-shot trigger and resolves when it finishes.
   * Lets caller `.finally()` to clear highlights.
   */
  static async playTrigger(asset: any): Promise<void> {
    let sound: Audio.Sound | null = null;
    try {
      const { sound: snd } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: false,
        volume: 0.02,
      });
      sound = snd;
      this.activeSounds.add(sound);
      await this.fadeIn(sound, 300, 0.8);

      return new Promise<void>((resolve) => {
        sound!.setOnPlaybackStatusUpdate((status: any) => {
          if (
            status.didJustFinish ||
            (!status.isPlaying && status.positionMillis > 0)
          ) {
            sound!.unloadAsync().catch(() => {});
            this.activeSounds.delete(sound!);
            resolve();
          }
        });
      });
    } catch (e) {
      console.log("Trigger sound play error:", e);
      if (sound) {
        try {
          await sound.unloadAsync();
        } catch {}
        this.activeSounds.delete(sound);
      }
      return Promise.resolve();
    }
  }
}

export default SoundManager;
