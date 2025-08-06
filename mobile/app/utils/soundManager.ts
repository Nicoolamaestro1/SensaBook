// app/utils/soundManager.ts
import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static activeSounds: Set<Audio.Sound> = new Set();

  // Zaustavi sve zvuke (carpet + trigger)
  static async stopAll() {
    try {
      if (this.carpetSound) {
        await this.carpetSound.stopAsync();
        await this.carpetSound.unloadAsync();
        this.carpetSound = null;
      }

      for (const sound of this.activeSounds) {
        try {
          await sound.stopAsync();
          await sound.unloadAsync();
        } catch (e) {}
      }
      this.activeSounds.clear();

      console.log("✅ All sounds stopped");
    } catch (error) {
      console.log("Error stopping sounds:", error);
    }
  }

  // Pusti carpet (uvek samo jedan)
  static async playCarpet(asset: any) {
    await this.stopCarpet(); // prvo ugasi stari

    const { sound } = await Audio.Sound.createAsync(asset, {
      shouldPlay: true,
      isLooping: true,
      volume: 0.5,
    });

    this.carpetSound = sound;
    console.log("🎵 Carpet sound started");
  }

  static async stopCarpet() {
    if (this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
        await this.carpetSound.unloadAsync();
      } catch (e) {}
      this.carpetSound = null;
      console.log("🛑 Carpet sound stopped");
    }
  }

  // Pusti trigger zvuk (može više njih paralelno)
  static async playTrigger(asset: any) {
    const { sound } = await Audio.Sound.createAsync(asset, {
      shouldPlay: true,
      isLooping: false,
      volume: 0.8,
    });

    this.activeSounds.add(sound);

    sound.setOnPlaybackStatusUpdate((status: any) => {
      if (status.didJustFinish) {
        sound.unloadAsync().catch(() => {});
        this.activeSounds.delete(sound);
      }
    });
  }
}

export default SoundManager;
