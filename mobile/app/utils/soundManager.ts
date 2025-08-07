import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading: boolean = false;

  static async fadeIn(sound: Audio.Sound, duration = 2000, targetVolume = 0.5) {
    const steps = 20;
    const stepTime = duration / steps;
    for (let i = 0; i <= steps; i++) {
      await sound.setVolumeAsync((i / steps) * targetVolume);
      await new Promise((res) => setTimeout(res, stepTime));
    }
  }

  static async fadeOut(sound: Audio.Sound, duration = 2000) {
    const status = await sound.getStatusAsync();
    if (!status.isLoaded) return;
    const initialVolume = status.volume ?? 1.0;
    const steps = 20;
    const stepTime = duration / steps;
    for (let i = steps; i >= 0; i--) {
      await sound.setVolumeAsync((i / steps) * initialVolume);
      await new Promise((res) => setTimeout(res, stepTime));
    }
    await sound.stopAsync();
    await sound.unloadAsync();
  }

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

  static async playCarpet(asset: any) {
    if (this.isCarpetLoading) return;
    this.isCarpetLoading = true;
    await this.stopCarpet();

    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: false,
        isLooping: true,
        volume: 0.0,
      });
      this.carpetSound = sound;

      await sound.playAsync();
      await this.fadeIn(sound, 1500, 0.5); // fade to 0.5 in 1.5s
      console.log("🎵 Carpet sound started (with fade in)");
    } catch (e) {
      console.log("Carpet play error:", e);
    } finally {
      this.isCarpetLoading = false;
    }
  }

  static async stopCarpet() {
    if (this.carpetSound) {
      try {
        await this.fadeOut(this.carpetSound, 1200);
        console.log("🛑 Carpet sound stopped (with fade out)");
      } catch (e) {
        // fallback: force stop/unload
        try {
          await this.carpetSound.stopAsync();
          await this.carpetSound.unloadAsync();
        } catch {}
      }
      this.carpetSound = null;
    }
  }

  static async playTrigger(asset: any) {
    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: false,
        volume: 0.8,
      });

      this.activeSounds.add(sound);
      await this.fadeIn(sound, 400, 0.8);

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
