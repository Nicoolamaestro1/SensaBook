import type { SoundAssetMap } from "../types/sounds";

import windyMountains from "../app/sounds/ambience/windy_mountains.mp3";
import defaultAmbience from "../app/sounds/ambience/default_ambience.mp3";
import tenseDrones from "../app/sounds/ambience/tense_drones.mp3";
import atmosphereSound from "../app/sounds/ambience/atmosphere-sound-effect-239969.mp3";
import thunderCity from "../app/sounds/ambience/thunder-city-377703.mp3";
import stormyNight from "../app/sounds/ambience/stormy_night.mp3";
import cabinRain from "../app/sounds/ambience/cabin_rain.mp3";
import cabin from "../app/sounds/ambience/cabin.mp3";

import footstepsApproaching from "../app/sounds/triggers/footsteps/footsteps-approaching-316715.mp3";
import storm from "../app/sounds/triggers/storm/storm.mp3";
import windHowl from "../app/sounds/triggers/wind/wind.mp3";
import rain from "../app/sounds/triggers/rain/rain.mp3";

/** --- Explicit families --- */
export const AMBIENCE_MAP = Object.freeze({
  "ambience/windy_mountains.mp3": windyMountains,
  "ambience/default_ambience.mp3": defaultAmbience,
  "ambience/tense_drones.mp3": tenseDrones,
  "ambience/atmosphere-sound-effect-239969.mp3": atmosphereSound,
  "ambience/thunder-city-377703.mp3": thunderCity,
  "ambience/stormy_night.mp3": stormyNight,
  "ambience/cabin_rain.mp3": cabinRain,
  "ambience/cabin.mp3": cabin,
} satisfies SoundAssetMap);

export const TRIGGER_MAP = Object.freeze({
  "triggers/footsteps-approaching-316715.mp3": footstepsApproaching,
  "triggers/storm.mp3": storm,
  "triggers/wind.mp3": windHowl,
  "triggers/rain.mp3": rain,
} satisfies SoundAssetMap);

/** --- Backward‑compat legacy keys (optional but handy) --- */
const LEGACY_KEYS = Object.freeze({
  // ambience (no folder)
  "windy_mountains.mp3": windyMountains,
  "default_ambience.mp3": defaultAmbience,
  "tense_drones.mp3": tenseDrones,
  "atmosphere-sound-effect-239969.mp3": atmosphereSound,
  "thunder-city-377703.mp3": thunderCity,
  "stormy_night.mp3": stormyNight,
  "cabin_rain.mp3": cabinRain,
  "cabin.mp3": cabin,

  // triggers (no folder)
  "footsteps-approaching-316715.mp3": footstepsApproaching,
  "storm.mp3": storm,
  "wind.mp3": windHowl,
  "rain.mp3": rain,

  // semantic fallbacks
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
} satisfies SoundAssetMap);

/** Combined view (for existing code) */
export const SOUND_MAP: SoundAssetMap = Object.freeze({
  ...AMBIENCE_MAP,
  ...TRIGGER_MAP,
  ...LEGACY_KEYS,
});

/** Word → trigger asset (not ambience!) */
export const WORD_TRIGGERS: Record<string, number> = Object.freeze({
  thunder: storm,
  footsteps: footstepsApproaching,
  wind: windHowl,
  storm: storm,
  rain: rain,
});

/** Types */
export type TriggerWord = {
  id: string;
  word: string;
  position: number;
  timing: number;
  soundKey?: string;
};

/** Utilities */
export const isAmbienceKey = (k?: string) =>
  !!k &&
  (k.startsWith("ambience/") ||
    k === "default_ambience.mp3" ||
    k === "ambience/default_ambience.mp3");

export const isTriggerKey = (k?: string) =>
  !!k && (k.startsWith("triggers/") || k in TRIGGER_MAP);

/** (Optional) Centralized key resolver to use across the app */
const EXTENSIONS = [".mp3", ".m4a", ".wav", ".ogg"] as const;

export function resolveSoundKey(raw?: string): string | undefined {
  if (!raw) return undefined;
  if (SOUND_MAP[raw]) return raw;

  const parts = raw.split("/");
  const basenameRaw = parts.pop() || raw;
  const baseNoExt = basenameRaw.replace(/\.[^/.]+$/, "");
  const folders = parts.length ? parts : [];

  const candidates: string[] = [];

  // same folder, with/without extension
  candidates.push(raw, baseNoExt);
  for (const e of EXTENSIONS) candidates.push(`${baseNoExt}${e}`);

  // check likely folders
  for (const dir of [...folders, "ambience", "triggers", ""]) {
    const p = dir ? `${dir}/` : "";
    candidates.push(`${p}${basenameRaw}`, `${p}${baseNoExt}`);
    for (const e of EXTENSIONS) candidates.push(`${p}${baseNoExt}${e}`);
  }

  // quick fuzzy fallbacks
  const hit = candidates.find((c) => SOUND_MAP[c]);
  if (hit) return hit;

  // last‑ditch: scan keys for basename matches
  const keys = Object.keys(SOUND_MAP);
  const fuzzy = keys.find(
    (k) =>
      k.endsWith(`/${baseNoExt}`) ||
      k.endsWith(`${baseNoExt}`) ||
      k.endsWith(`${baseNoExt}.mp3`) ||
      k.includes(`/${baseNoExt}.`)
  );
  return fuzzy;
}
