// app/utils/soundManager.ts
import { Audio } from "expo-av";

class SoundManager {
  private static carpetSound: Audio.Sound | null = null;
  private static activeSounds: Set<Audio.Sound> = new Set();
  private static isCarpetLoading: boolean = false;

  /**
   * Stop and unload ALL sounds (carpet + trigger).
   */
  static async stopAll() {
    // Stop carpet
    await this.stopCarpet();
    // Stop all triggers
    for (const sound of this.activeSounds) {
      try {
        await sound.stopAsync();
        await sound.unloadAsync();
      } catch (e) {}
    }
    this.activeSounds.clear();
    console.log("✅ All sounds stopped");
  }

  /**
   * Play looping ambient sound. Stops previous carpet if exists.
   * Ignores rapid repeated calls using a loading lock.
   */
  static async playCarpet(asset: any) {
    if (this.isCarpetLoading) return; // ignore rapid repeated calls
    this.isCarpetLoading = true;
    await this.stopCarpet();

    try {
      const { sound } = await Audio.Sound.createAsync(asset, {
        shouldPlay: true,
        isLooping: true,
        volume: 0.5,
      });
      this.carpetSound = sound;
      console.log("🎵 Carpet sound started");
    } catch (e) {
      console.log("Carpet play error:", e);
    } finally {
      this.isCarpetLoading = false;
    }
  }

  /**
   * Stops only the carpet (ambient) sound.
   */
  static async stopCarpet() {
    if (this.carpetSound) {
      try {
        await this.carpetSound.stopAsync();
        await this.carpetSound.unloadAsync();
        console.log("🛑 Carpet sound stopped");
      } catch (e) {
        console.log("Carpet stop error:", e);
      }
      this.carpetSound = null;
    }
  }

  /**
   * Play one-shot trigger sound (does not loop).
   */
  static async playTrigger(asset: any) {
    try {
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
    } catch (e) {
      console.log("Trigger sound play error:", e);
    }
  }
}

export default SoundManager;
