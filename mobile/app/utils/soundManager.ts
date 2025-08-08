import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading: boolean = false;

  // Smooth fade-in effect with shorter duration and fewer steps for seamless experience
  static async fadeIn(sound: Audio.Sound, duration = 1200, targetVolume = 0.5) {
    const steps = 10;
    const stepTime = duration / steps;

    // Set initial volume immediately after play, so the sound is not completely silent
    await sound.setVolumeAsync(0.02);

    for (let i = 1; i <= steps; i++) {
      const volume = (i / steps) * targetVolume;
      await sound.setVolumeAsync(volume);
      await new Promise((res) => setTimeout(res, stepTime));
    }
  }

  // Smooth fade-out effect, faster for responsive UI
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

  // Stops all active sounds, including carpet and triggers
  static async stopAll() {
    await this.stopCarpet();
    for (const sound of this.activeSounds) {
      try {
        await sound.stopAsync();
        await sound.unloadAsync();
      } catch (e) {}
    }
    this.activeSounds.clear();
    console.log("✅ All sounds stopped");
  }

  // Plays the looping carpet/background sound with fade-in
  static async playCarpet(asset: any) {
    if (this.isCarpetLoading) return;
    this.isCarpetLoading = true;
    await this.stopCarpet();

    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: false,
        isLooping: true,
        volume: 0.02, // Start quietly for instant audio feedback
      });
      this.carpetSound = sound;

      await sound.playAsync();
      await this.fadeIn(sound, 1200, 0.5); // Fade up to 0.5 in 1.2s
      console.log("🎵 Carpet sound started (with fade in)");
    } catch (e) {
      console.log("Carpet play error:", e);
    } finally {
      this.isCarpetLoading = false;
    }
  }

  // Stops the carpet/background sound with fade-out
  static async stopCarpet() {
    if (this.carpetSound) {
      try {
        await this.fadeOut(this.carpetSound, 800);
        console.log("🛑 Carpet sound stopped (with fade out)");
      } catch (e) {
        // Fallback: force stop/unload if fade fails
        try {
          await this.carpetSound.stopAsync();
          await this.carpetSound.unloadAsync();
        } catch {}
      }
      this.carpetSound = null;
    }
  }

  /**
   * Plays a one-shot trigger sound (not looping).
   */
  static async playTrigger(asset: any) {
    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: false,
        volume: 0.02, // Start quietly
      });

      this.activeSounds.add(sound);
      await this.fadeIn(sound, 300, 0.8); // Quick fade-in for trigger sound

      sound.setOnPlaybackStatusUpdate((status: any) => {
        if (status.didJustFinish) {
          sound.unloadAsync().catch(() => {});
          this.activeSounds.delete(sound);
        }
      });
    } catch (e) {
      console.log("Trigger sound play error:", e);
    }
  }
}

export default SoundManager;
