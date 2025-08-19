export type TriggeredSoundFromApi = {
  word: string;
  position?: number;
  file?: string;
  word_position?: number;
  sound?: string;
};

export type SoundscapeResponse = {
  book_id: number;
  book_page_id: string;
  summary: string;
  detected_scenes: string[];
  scene_keyword_counts: Record<string, number>;
  scene_keyword_positions: Record<string, number[]>;
  carpet_tracks: string[];
  triggered_sounds: TriggeredSoundFromApi[];
};
