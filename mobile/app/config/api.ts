// app/config/api.ts
import { Platform } from "react-native";

export const API_HOST =
  Platform.OS === "android" ? "http://10.0.2.2:8000" : "http://127.0.0.1:8000";

export const API_BASE = `${API_HOST}/soundscape`;

export function buildSoundscapeUrl(
  bookId: number | string,
  chapterNumber: number,
  pageNumber: number
) {
  return `${API_BASE}/book/${bookId}/chapter${chapterNumber}/page/${pageNumber}`;
}

// Optional: one-liner debug logger so you always see the exact URL
export function logSoundscapeRequest(
  bookId: number | string,
  chapter: number,
  page: number
) {
  // keep this as a single template so it’s easy to grep
  console.log(`[API] GET ${buildSoundscapeUrl(bookId, chapter, page)}`);
}
