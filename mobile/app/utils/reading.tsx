import { WORD_TRIGGERS, isAmbienceKey } from "../../constants/sounds";
import type { TriggerWord } from "../../constants/sounds";
import type { SoundscapeResponse } from "../../types/soundscape";
import { buildSoundscapeUrl } from "../config/api";

export function calculateWordTiming(text: string, wpm: number) {
  if (!text) return { words: [], msPerWord: 333 };
  const words = text.trim().split(/\s+/);
  const msPerWord = (60 / Math.max(wpm || 0, 1)) * 1000;
  return { words, msPerWord };
}

export function findTriggerWords(
  words: string[],
  msPerWord: number
): TriggerWord[] {
  return words
    .map((word, index) => {
      const clean = word.replace(/[^\w\s]/gi, "").toLowerCase();
      if (WORD_TRIGGERS[clean]) {
        return {
          id: `${index}`,
          word: clean,
          position: index,
          timing: index * msPerWord,
        };
      }
      return null;
    })
    .filter((t): t is TriggerWord => t !== null);
}

export function filterNonAmbienceSounds(keys: string[]) {
  return keys.filter((k) => !isAmbienceKey(k));
}

export async function fetchSoundscape(
  bookId: number,
  chapterNumber: number,
  pageNumber: number
): Promise<SoundscapeResponse> {
  const url = buildSoundscapeUrl(bookId, chapterNumber, pageNumber); // <-- NEW
  const res = await fetch(url);
  if (!res.ok) throw new Error(`soundscape ${res.status} for ${url}`);
  return res.json();
}

// --- tokenization & alignment helpers (pure) ---
export function norm(w: string) {
  return w
    .replace(/\u00AD/g, "")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, "");
}

export function tokenize(text: string) {
  return text
    .replace(/\u00AD/g, "")
    .split(/\s+/)
    .filter(Boolean);
}

export function snapToNearestToken(
  tokens: string[],
  targetWord: string,
  approxIdx: number,
  window = 2
) {
  const target = norm(targetWord);
  if (tokens[approxIdx] && norm(tokens[approxIdx]) === target) return approxIdx;
  for (let d = 1; d <= window; d++) {
    const L = approxIdx - d;
    const R = approxIdx + d;
    if (L >= 0 && norm(tokens[L] || "") === target) return L;
    if (R < tokens.length && norm(tokens[R] || "") === target) return R;
  }
  return approxIdx;
}

// --- pagination & progress (already in your file if you added them) ---
export function paginateText(
  text: string,
  viewport: { width: number; height: number },
  typography: { fontSize: number; lineHeight: number }
): string[] {
  const words = text.split(/\s+/).filter(Boolean);
  const usableHeight = viewport.height * 0.9;
  const linesPerPage = Math.floor(usableHeight / typography.lineHeight);
  const avgCharsPerWord = 6;
  const charsPerLine = Math.floor(viewport.width / (typography.fontSize * 0.6));
  const wordsPerLine = Math.floor(charsPerLine / avgCharsPerWord);
  const wordsPerPage = linesPerPage * wordsPerLine;

  const pages: string[] = [];
  for (let i = 0; i < words.length; i += wordsPerPage) {
    pages.push(words.slice(i, i + wordsPerPage).join(" "));
  }
  return pages;
}

export function computeReadingProgress(
  book: import("../../types/book").Book,
  currentChapterIndex: number,
  currentPageIndex: number
) {
  const totalPagesInBook =
    book?.chapters?.reduce(
      (total, chapter) => total + chapter.pages.length,
      0
    ) || 0;

  const currentPageInBook =
    (book?.chapters
      ?.slice(0, currentChapterIndex)
      .reduce((total, chapter) => total + chapter.pages.length, 0) || 0) +
      currentPageIndex +
      1 || 0;

  const progress =
    totalPagesInBook > 0 ? currentPageInBook / totalPagesInBook : 0;
  return { totalPagesInBook, currentPageInBook, progress };
}
