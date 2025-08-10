import windyMountains from "../app/sounds/ambience/windy_mountains.mp3";
import defaultAmbience from "../app/sounds/ambience/default_ambience.mp3";
import tenseDrones from "../app/sounds/ambience/tense_drones.mp3";
import footstepsApproaching from "../app/sounds/triggers/footsteps/footsteps-approaching-316715.mp3";
import atmosphereSound from "../app/sounds/ambience/atmosphere-sound-effect-239969.mp3";
import thunderCity from "../app/sounds/ambience/thunder-city-377703.mp3";
import stormyNight from "../app/sounds/ambience/stormy_night.mp3";
import storm from "../app/sounds/triggers/storm/storm.mp3";
import cabinRain from "../app/sounds/ambience/cabin_rain.mp3";
import cabin from "../app/sounds/ambience/cabin.mp3";
import windHowl from "../app/sounds/triggers/wind/wind.mp3";

export const SOUND_MAP: Record<string, any> = {
  // Ambience sounds (carpet sounds)
  "ambience/windy_mountains.mp3": windyMountains,
  "ambience/default_ambience.mp3": defaultAmbience,
  "ambience/tense_drones.mp3": tenseDrones,
  "ambience/atmosphere-sound-effect-239969.mp3": atmosphereSound,
  "ambience/thunder-city-377703.mp3": thunderCity,
  "ambience/stormy_night.mp3": stormyNight,
  "ambience/cabin_rain.mp3": cabinRain, // Indoor cabin sound with rain
  "ambience/cabin.mp3": cabin, // Indoor cabin sound without rain

  // Trigger sounds
  "triggers/footsteps-approaching-316715.mp3": footstepsApproaching,
  "triggers/storm.mp3": storm,
  "triggers/wind.mp3": windHowl,

  // Legacy mappings for backward compatibility
  "windy_mountains.mp3": windyMountains,
  "default_ambience.mp3": defaultAmbience,
  "tense_drones.mp3": tenseDrones,
  "footsteps-approaching-316715.mp3": footstepsApproaching,
  "atmosphere-sound-effect-239969.mp3": atmosphereSound,
  "thunder-city-377703.mp3": thunderCity,
  "stormy_night.mp3": stormyNight,
  "storm.mp3": storm,
  "cabin_rain.mp3": cabinRain,
  "cabin.mp3": cabin,
  "restaurant_murmur.mp3": atmosphereSound,
  "hotel_lobby.mp3": atmosphereSound,
  "quiet_museum.mp3": defaultAmbience,
  "horse_carriage.mp3": footstepsApproaching,
  "stone_echoes.mp3": tenseDrones,
  "night_forest.mp3": windyMountains,
  "indoors.mp3": cabinRain,
  "inside.mp3": cabinRain,
  "house.mp3": cabinRain,
  "room.mp3": cabinRain,
  "building.mp3": cabinRain,
  "apartment.mp3": cabinRain,
  "home.mp3": cabinRain,
  "wind.mp3": windHowl,
};

export const WORD_TRIGGERS: Record<string, any> = {
  thunder: thunderCity,
  footsteps: footstepsApproaching,
  wind: windHowl,
  storm: storm,
};

export type TriggerWord = {
  id: string;
  word: string;
  position: number;
  timing: number;
};
