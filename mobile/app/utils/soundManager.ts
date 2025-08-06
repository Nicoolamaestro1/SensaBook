// app/utils/soundManager.ts
import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static activeSounds: Set<Audio.Sound> = new Set();

  static async fadeIn(sound: Audio.Sound, duration = 2000) {
    const steps = 20;
    const stepTime = duration / steps;
    for (let i = 0; i <= steps; i++) {
      await sound.setVolumeAsync(i / steps);
      await new Promise((res) => setTimeout(res, stepTime));
    }
  };
  
  static async fadeOut(sound: Audio.Sound, duration = 2000) {
    const steps = 20;
    const stepTime = duration / steps;
    for (let i = steps; i >= 0; i--) {
      await sound.setVolumeAsync(i / steps);
      await new Promise((res) => setTimeout(res, stepTime));
    }
    await sound.stopAsync();
    await sound.unloadAsync();
  };

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
      if (this.carpetSound) {
        await this.fadeOut(this.carpetSound);
      }

      console.log("✅ All sounds stopped");
    } catch (error) {
      console.log("Error stopping sounds:", error);
    }
  }

  static async playCarpet(asset: any) {
    await this.stopCarpet();

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

  static async playTrigger(asset: any) {
    const { sound } = await Audio.Sound.createAsync(asset, {
      shouldPlay: true,
      isLooping: false,
      volume: 0.8,
    });

    this.activeSounds.add(sound);
    await this.fadeIn(sound);

    sound.setOnPlaybackStatusUpdate((status: any) => {
      if (status.didJustFinish) {
        sound.unloadAsync().catch(() => {});
        this.activeSounds.delete(sound);
      }
    });
  }
}

export default SoundManager;
