import React from "react";
import { useLocalSearchParams, useRouter, useFocusEffect } from "expo-router";
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  AppState,
  Dimensions,
  Platform,
} from "react-native";
import { ProgressBar } from "react-native-paper";
import Animated, {
  useSharedValue,
  withTiming,
  useAnimatedStyle,
} from "react-native-reanimated";
import SoundManager from "../utils/soundManager";
import { useBook } from "../../hooks/useBooks";
import { useWpm } from "../../hooks/useWpm";
import { WORD_TRIGGERS, TriggerWord, SOUND_MAP } from "../../constants/sounds";
import CrossPlatformSlider from "../components/CrossPlatformSlider";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import AsyncStorage from "@react-native-async-storage/async-storage";

/* =====================================================
   THEME & CONSTANTS
   ===================================================== */

const COLORS = {
  card: "#17171c",
  text: "#EAEAF0",
  subtext: "#A6A8B1",
  border: "rgba(255,255,255,0.06)",
  accent: "#FF7A18",
};

const STORAGE_KEYS = {
  wpm: "settings.wpm",
  ambVol: "settings.ambienceVolPct",
  trigVol: "settings.triggerVolPct",
};

const { height, width } = Dimensions.get("window");
const API_HOST = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
const API_BASE = `${API_HOST}/soundscape`;

/* =====================================================
   TYPES
   ===================================================== */

type SoundscapeResponse = {
  book_id: number;
  book_page_id: number;
  summary: string;
  detected_scenes: string[];
  scene_keyword_counts: Record<string, number>;
  scene_keyword_positions: Record<string, number[]>;
  carpet_tracks: string[];
  triggered_sounds: Array<{ word: string; position: number; file: string }>; // NOTE: API sometimes uses different keys; we normalize later
};

type TimeoutId = ReturnType<typeof setTimeout>;

/* =====================================================
   HELPERS (pure)
   ===================================================== */

function norm(w: string) {
  return w.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "");
}

function tokenize(text: string) {
  return text.split(/\s+/).filter(Boolean);
}

function snapToNearestToken(
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

function resolveSoundKey(soundFromApi?: string): string | undefined {
  if (!soundFromApi) return undefined;
  if ((SOUND_MAP as any)[soundFromApi]) return soundFromApi;

  const parts = soundFromApi.split("/");
  const baseRaw = parts.pop() || soundFromApi;
  const folders = parts.length ? parts : [];
  const baseNoExt = baseRaw.replace(/\.[^/.]+$/, "");
  const exts = [".mp3", ".m4a", ".wav", ".ogg"];

  const candidates: string[] = [];
  for (const dir of [...folders, "ambience", "triggers", ""]) {
    const p = dir ? `${dir}/` : "";
    candidates.push(`${p}${baseRaw}`, `${p}${baseNoExt}`);
    for (const e of exts) candidates.push(`${p}${baseNoExt}${e}`);
  }
  candidates.push(baseNoExt);
  for (const e of exts) candidates.push(`${baseNoExt}${e}`);

  for (const c of candidates) {
    if ((SOUND_MAP as any)[c]) return c;
  }

  const keys = Object.keys(SOUND_MAP as any);
  const fuzzy = keys.find(
    (k) =>
      k.endsWith(`/${baseNoExt}`) ||
      k.endsWith(`${baseNoExt}`) ||
      k.endsWith(`${baseNoExt}.mp3`) ||
      k.includes(`/${baseNoExt}.`)
  );
  if (fuzzy) return fuzzy;

  return undefined;
}

async function fetchSoundscape(
  bookId: string | number,
  chapterNumber: number,
  pageNumber: number
): Promise<SoundscapeResponse> {
  const res = await fetch(
    `${API_BASE}/book/${bookId}/chapter${chapterNumber}/page/${pageNumber}`
  );
  if (!res.ok) throw new Error(`soundscape ${res.status}`);
  return res.json();
}

/* =====================================================
   COMPONENT
   ===================================================== */

export default function BookDetailScreen() {
  /* ---------- Navigation & Safe Area ---------- */
  const params = useLocalSearchParams();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  /* ---------- Animation State ---------- */
  const CLOSED_EXTRA = 40; // push closed panel farther offscreen
  const translateY = useSharedValue(-10000);
  const openProg = useSharedValue(0);
  const hasMeasuredRef = React.useRef(false);

  /* ---------- UI Local State ---------- */
  const [optionsOpen, setOptionsOpen] = React.useState(false);
  const [hasShownPanel, setHasShownPanel] = React.useState(false);
  const [optionsHeight, setOptionsHeight] = React.useState(0);

  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(
    Number(params.chapter ?? 0)
  );
  const [currentPageIndex, setCurrentPageIndex] = React.useState(
    Number(params.page ?? 0)
  );
  const [currentChunkIndex, setCurrentChunkIndex] = React.useState(
    Number(params.chunk ?? 0)
  );

  const [paginatedChunks, setPaginatedChunks] = React.useState<string[]>([]);
  const [triggerWords, setTriggerWords] = React.useState<TriggerWord[]>([]);
  const [activeTriggerWords, setActiveTriggerWords] = React.useState<
    Set<string>
  >(new Set());
  const [activeWordIndex, setActiveWordIndex] = React.useState<number | null>(
    null
  );

  // Volumes (percent) + WPM
  const [ambienceVolPct, setAmbienceVolPct] = React.useState(60);
  const [triggerVolPct, setTriggerVolPct] = React.useState(80);
  const { wpm, setWpm } = useWpm();

  // Refs for timers/indices
  const wpmRef = React.useRef(wpm);
  React.useEffect(() => {
    wpmRef.current = wpm;
  }, [wpm]);

  const triggerWordsRef = React.useRef<TriggerWord[]>([]);
  React.useEffect(() => {
    triggerWordsRef.current = triggerWords;
  }, [triggerWords]);

  const currentWordIndexRef = React.useRef(0);
  React.useEffect(() => {
    if (activeWordIndex != null) currentWordIndexRef.current = activeWordIndex;
  }, [activeWordIndex]);

  const firedTriggerIdsRef = React.useRef<Set<string>>(new Set());
  const wordTimeoutRef = React.useRef<TimeoutId | null>(null);

  /* ---------- Data: Book ---------- */
  const { bookId } = params;
  const { book, loading } = useBook(bookId as string) as {
    book: any;
    loading: boolean;
  };

  const currentChapter = book?.chapters?.[currentChapterIndex];
  const currentPage = currentChapter?.pages?.[currentPageIndex];
  const totalChapters = book?.chapters?.length || 0;
  const totalPages = currentChapter?.pages?.length || 0;

  /* =====================================================
     ANIMATIONS
     ===================================================== */
  const optionsAnim = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
    opacity: openProg.value,
    shadowOpacity: 0.35 * openProg.value,
    elevation: 10 * openProg.value,
  }));

  React.useEffect(() => {
    if (!hasMeasuredRef.current) return;
    const closedY = -(optionsHeight + insets.top + CLOSED_EXTRA);
    translateY.value = withTiming(optionsOpen ? 0 : closedY, { duration: 250 });
    openProg.value = withTiming(optionsOpen ? 1 : 0, { duration: 200 });
  }, [optionsOpen, optionsHeight, insets.top]);

  /* =====================================================
     PERSIST SETTINGS (AsyncStorage)
     ===================================================== */

  // Load stored values on mount
  React.useEffect(() => {
    (async () => {
      try {
        const [w, a, t] = await Promise.all([
          AsyncStorage.getItem(STORAGE_KEYS.wpm),
          AsyncStorage.getItem(STORAGE_KEYS.ambVol),
          AsyncStorage.getItem(STORAGE_KEYS.trigVol),
        ]);
        if (w) setWpm(Math.max(50, Math.min(600, Number(w))));
        if (a) {
          const n = Math.max(0, Math.min(100, Number(a)));
          setAmbienceVolPct(n);
          SoundManager.setCarpetVolume(n / 100);
        }
        if (t) {
          const n = Math.max(0, Math.min(100, Number(t)));
          setTriggerVolPct(n);
          SoundManager.setTriggerVolume(n / 100);
        }
      } catch {}
    })();
  }, [setWpm]);

  // Simple saver helper
  const save = React.useCallback(
    (key: string, value: number | string) =>
      AsyncStorage.setItem(key, String(value)).catch(() => {}),
    []
  );

  /* =====================================================
     URL SYNC (expo-router)
     ===================================================== */

  useFocusEffect(
    React.useCallback(() => {
      router.setParams({
        chapter: String(currentChapterIndex),
        page: String(currentPageIndex),
        chunk: String(currentChunkIndex),
      });
    }, [currentChapterIndex, currentPageIndex, currentChunkIndex, router])
  );

  React.useEffect(() => {
    if (params.chapter !== undefined)
      setCurrentChapterIndex(Number(params.chapter));
    if (params.page !== undefined) setCurrentPageIndex(Number(params.page));
    if (params.chunk !== undefined) setCurrentChunkIndex(Number(params.chunk));
  }, [params.chapter, params.page, params.chunk]);

  /* =====================================================
     TEXT PAGINATION & TIMING
     ===================================================== */

  const paginateText = React.useCallback(
    (text: string, fontSize = 16, lineHeight = 24) => {
      const words = text.split(/\s+/).filter(Boolean);
      const usableHeight = height * 0.9;
      const linesPerPage = Math.floor(usableHeight / lineHeight);
      const avgCharsPerWord = 6;
      const charsPerLine = Math.floor(width / (fontSize * 0.6));
      const wordsPerLine = Math.floor(charsPerLine / avgCharsPerWord);
      const wordsPerPage = linesPerPage * wordsPerLine;

      const pages: string[] = [];
      for (let i = 0; i < words.length; i += wordsPerPage) {
        pages.push(words.slice(i, i + wordsPerPage).join(" "));
      }
      return pages;
    },
    []
  );

  const calculateWordTiming = React.useCallback((text: string) => {
    if (!text) return { words: [], msPerWord: 333 };
    const words = text.split(/\s+/).filter(Boolean);
    const msPerWord = 60000 / (wpmRef.current || 200);
    return { words, msPerWord };
  }, []);

  const findTriggerWords = React.useCallback(
    (text: string) => {
      const { words, msPerWord } = calculateWordTiming(text);
      return words
        .map((word, index) => {
          const clean = word.toLowerCase().replace(/[^\w]/g, "");
          if ((WORD_TRIGGERS as any)[clean]) {
            return {
              id: `${index}`,
              word: clean,
              position: index,
              timing: index * msPerWord,
            } as TriggerWord;
          }
          return null;
        })
        .filter(Boolean) as TriggerWord[];
    },
    [calculateWordTiming]
  );

  /* =====================================================
     TIMERS / PLAYBACK CONTROL
     ===================================================== */

  const stopReadingTimer = React.useCallback(() => {
    if (wordTimeoutRef.current) {
      clearTimeout(wordTimeoutRef.current);
      wordTimeoutRef.current = null;
    }
  }, []);

  const startReadingTimer = React.useCallback(
    (resumeFromIndex?: number, triggersArg?: TriggerWord[]) => {
      stopReadingTimer();
      const chunk = paginatedChunks[currentChunkIndex] || "";
      const words = chunk.split(/\s+/).filter(Boolean);
      const msPerWord = 60000 / (wpmRef.current || 200);

      const sourceTriggers = triggersArg ?? triggerWordsRef.current;
      const triggerMap = new Map<number, TriggerWord>();
      sourceTriggers.forEach((t) => triggerMap.set(t.position, t));

      const startIndex = resumeFromIndex ?? 0;
      setActiveWordIndex(startIndex);
      currentWordIndexRef.current = startIndex;
      setActiveTriggerWords(new Set());

      let idx = startIndex;
      const tick = () => {
        const trig = triggerMap.get(idx);
        if (trig) {
          setActiveTriggerWords((prev) => new Set(prev).add(trig.id));

          console.log(
            `Trigger fired: word="${trig.word}", position=${
              trig.position
            }, soundKey="${trig.soundKey ?? "(none)"}"`
          );

          const assetKey = trig.soundKey ?? trig.word;
          console.log(`Resolved assetKey: "${assetKey}"`);

          if (
            typeof assetKey === "string" &&
            assetKey.startsWith("ambience/")
          ) {
            console.log(
              `Skipping ambience trigger for "${trig.word}" (assetKey: "${assetKey}")`
            );
            setActiveTriggerWords((prev) => {
              const s = new Set(prev);
              s.delete(trig.id);
              return s;
            });
          } else {
            const asset =
              (SOUND_MAP as any)[assetKey] ?? (WORD_TRIGGERS as any)[trig.word];

            if (asset) {
              console.log(
                `✅ Playing sound for "${trig.word}" using key "${assetKey}"`
              );
              SoundManager.playTrigger(asset).finally(() => {
                setActiveTriggerWords((prev) => {
                  const s = new Set(prev);
                  s.delete(trig.id);
                  return s;
                });
              });
            } else {
              console.warn(
                `⚠️ No sound found for trigger: "${trig.word}" (assetKey: "${assetKey}")`
              );
              setActiveTriggerWords((prev) => {
                const s = new Set(prev);
                s.delete(trig.id);
                return s;
              });
            }
          }
        }

        setActiveWordIndex(idx);
        currentWordIndexRef.current = idx;
        idx++;
        if (idx < words.length) {
          wordTimeoutRef.current = setTimeout(tick, msPerWord);
        } else {
          stopReadingTimer();
        }
      };

      wordTimeoutRef.current = setTimeout(tick, msPerWord);
    },
    [paginatedChunks, currentChunkIndex, stopReadingTimer]
  );
  const [lastCarpet, setLastCarpet] = React.useState<{
    key?: string;
    asset?: number;
  } | null>(null);

  const ensureAmbienceAfterGesture = React.useCallback(() => {
    if (lastCarpet?.asset) {
      // Safe to call repeatedly; playCarpet will no-op if already playing
      SoundManager.playCarpet(lastCarpet.asset, lastCarpet.key);
    }
  }, [lastCarpet]);

  /* =====================================================
     OPTIONS PANEL OPEN/CLOSE
     ===================================================== */

  const openOptions = React.useCallback(() => {
    ensureAmbienceAfterGesture();
    stopReadingTimer();
    setHasShownPanel(true);
    setOptionsOpen(true);
  }, [ensureAmbienceAfterGesture, stopReadingTimer]);

  const closeOptions = React.useCallback(() => {
    setOptionsOpen(false);
    startReadingTimer(currentWordIndexRef.current ?? 0);
  }, [startReadingTimer]);

  /* =====================================================
     NAVIGATION HANDLERS (prev/next)
     ===================================================== */

  const goToNextPage = React.useCallback(() => {
    stopReadingTimer();
    ensureAmbienceAfterGesture();
    if (currentChunkIndex < paginatedChunks.length - 1) {
      setCurrentChunkIndex((i) => i + 1);
      return;
    }
    if (currentPageIndex < totalPages - 1) {
      setCurrentPageIndex((i) => i + 1);
      setCurrentChunkIndex(0);
    } else if (currentChapterIndex < totalChapters - 1) {
      setCurrentChapterIndex((i) => i + 1);
      setCurrentPageIndex(0);
      setCurrentChunkIndex(0);
    }
  }, [
    ensureAmbienceAfterGesture,
    stopReadingTimer,
    currentChunkIndex,
    paginatedChunks.length,
    currentPageIndex,
    totalPages,
    currentChapterIndex,
    totalChapters,
  ]);

  const goToPreviousPage = React.useCallback(() => {
    stopReadingTimer();
    ensureAmbienceAfterGesture();
    if (
      currentChapterIndex === 0 &&
      currentPageIndex === 0 &&
      currentChunkIndex === 0
    ) {
      router.replace("/library");
      return;
    }
    if (currentChunkIndex > 0) {
      setCurrentChunkIndex((i) => i - 1);
      return;
    }
    if (currentPageIndex > 0) {
      setCurrentPageIndex((i) => i - 1);
      setCurrentChunkIndex(0);
    } else if (currentChapterIndex > 0) {
      const prevChapter = book?.chapters?.[currentChapterIndex - 1];
      const lastPageIndex = (prevChapter?.pages?.length || 1) - 1;
      setCurrentChapterIndex((i) => i - 1);
      setCurrentPageIndex(lastPageIndex);
      setCurrentChunkIndex(0);
    }
  }, [
    ensureAmbienceAfterGesture,
    stopReadingTimer,
    currentChapterIndex,
    currentPageIndex,
    currentChunkIndex,
    router,
    book?.chapters,
  ]);

  /* =====================================================
     SOUNDSCAPE LOADING (API + fallback)
     ===================================================== */

  const loadSoundscapeForPage = React.useCallback(
    async (chapterIndex?: number, pageIndex?: number) => {
      if (!book) return;

      const ci = chapterIndex ?? currentChapterIndex;
      const pi = pageIndex ?? currentPageIndex;

      const chapterNumber = book.chapters?.[ci]?.chapter_number ?? ci + 1;
      const pageNumber =
        book.chapters?.[ci]?.pages?.[pi]?.page_number ?? pi + 1;

      const url = `${API_BASE}/book/${bookId}/chapter${chapterNumber}/page/${pageNumber}`;
      console.log(`[API Request] Fetching soundscape: ${url}`);

      try {
        const data = await fetchSoundscape(
          bookId as string,
          chapterNumber,
          pageNumber
        );

        const chunkText = paginatedChunks[currentChunkIndex] || "";
        const chunkTokens = tokenize(chunkText);
        const wordsBeforeThisChunk = paginatedChunks
          .slice(0, currentChunkIndex)
          .reduce((sum, ch) => sum + tokenize(ch).length, 0);

        const chunkTriggers: TriggerWord[] = (
          (data as any).triggered_sounds || []
        )
          .map((t: any, i: number) => {
            const absolutePos = Number(
              (t as any).word_position ?? t.position ?? 0
            );
            const approxInChunk = absolutePos - wordsBeforeThisChunk;
            const snapped = snapToNearestToken(
              chunkTokens,
              String(t.word || ""),
              approxInChunk,
              2
            );

            const rawKey = resolveSoundKey((t as any).sound);
            const safeKey =
              rawKey && rawKey.startsWith("ambience/") ? undefined : rawKey;

            return {
              id: String(i),
              word: String(t.word || "").toLowerCase(),
              position: snapped,
              timing: 0,
              soundKey: safeKey,
            } as any as TriggerWord;
          })
          .filter(
            (tw: TriggerWord) =>
              tw.position >= 0 && tw.position < chunkTokens.length
          );

        setTriggerWords(chunkTriggers);
        stopReadingTimer();
        startReadingTimer(0, chunkTriggers);

        const first = (data as any).carpet_tracks?.[0];
        const resolved = resolveSoundKey(first);
        if (resolved && (SOUND_MAP as any)[resolved]) {
          const asset = (SOUND_MAP as any)[resolved];
          setLastCarpet({ key: resolved, asset }); // remember for retries
          await SoundManager.playCarpet(asset, resolved);
        }
        return;
      } catch (err) {
        console.log("Soundscape API fallback:", err);
      }

      // fallback to local mapping if API fails
      const page = book?.chapters?.[ci]?.pages?.[pi];
      let ambienceKey = page?.ambient as string;
      if (!ambienceKey) {
        const pageAmbienceMap: Record<string, string> = {
          "0-0": "ambience/windy_mountains.mp3",
          "0-1": "ambience/cabin_rain.mp3",
          "1-0": "ambience/stormy_night.mp3",
        };
        ambienceKey =
          pageAmbienceMap[`${ci}-${pi}`] || "ambience/default_ambience.mp3";
      }
      const asset = (SOUND_MAP as any)[ambienceKey];
      if (asset) {
        setLastCarpet({ key: ambienceKey, asset });
        await SoundManager.playCarpet(asset, ambienceKey);
      }
    },
    [
      book,
      bookId,
      currentChapterIndex,
      currentPageIndex,
      currentChunkIndex,
      paginatedChunks,
      startReadingTimer,
      stopReadingTimer,
    ]
  );

  /* =====================================================
     EFFECTS / LIFECYCLE
     ===================================================== */

  // stop carpet when switching books
  React.useEffect(() => {
    return () => {
      SoundManager.stopCarpet();
    };
  }, [bookId]);

  // paginate when page changes
  React.useEffect(() => {
    if (book && currentPage) {
      const chunks = paginateText(currentPage.content);
      setPaginatedChunks(chunks);
      setCurrentChunkIndex(0);
    }
  }, [book, currentChapterIndex, currentPageIndex, currentPage, paginateText]);

  // recompute triggers & start timers when chunk changes
  React.useEffect(() => {
    if (
      book &&
      book.chapters?.[currentChapterIndex]?.pages?.[currentPageIndex] &&
      paginatedChunks.length > 0
    ) {
      const chunk = paginatedChunks[currentChunkIndex];
      const triggers = findTriggerWords(chunk);
      setTriggerWords(triggers);
      firedTriggerIdsRef.current = new Set();
      setActiveTriggerWords(new Set());
      setActiveWordIndex(0);

      loadSoundscapeForPage(currentChapterIndex, currentPageIndex);
      startReadingTimer(0, triggers);
    }
  }, [
    book,
    currentChapterIndex,
    currentPageIndex,
    currentChunkIndex,
    paginatedChunks,
    findTriggerWords,
    loadSoundscapeForPage,
    startReadingTimer,
  ]);

  // restart timer on WPM changes
  React.useEffect(() => {
    if (paginatedChunks.length > 0) {
      startReadingTimer(currentWordIndexRef.current ?? 0);
    }
  }, [wpm, startReadingTimer, paginatedChunks.length]);

  // cleanup on screen blur
  useFocusEffect(
    React.useCallback(
      () => () => {
        SoundManager.stopAll();
        stopReadingTimer();
      },
      [stopReadingTimer]
    )
  );

  // ensure SoundManager volumes match UI defaults (once)
  React.useEffect(() => {
    SoundManager.setCarpetVolume(ambienceVolPct / 100);
    SoundManager.setTriggerVolume(triggerVolPct / 100);
  }, []);

  // pause audio/timer when app backgrounds
  React.useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => {
      if (s === "background" || s === "inactive") {
        SoundManager.stopAll();
        stopReadingTimer();
      }
    });
    return () => sub.remove();
  }, [stopReadingTimer]);

  /* =====================================================
     UI HELPERS
     ===================================================== */

  const renderTextWithHighlights = (text: string) => {
    const words = text.split(/\s+/).filter(Boolean);
    return (
      <Text style={styles.pageText}>
        {words.map((word, index) => {
          const trigger = triggerWords.find((t) => t.position === index);
          const isActiveTrigger = trigger
            ? activeTriggerWords.has(trigger.id)
            : false;
          const isActiveReading = activeWordIndex === index;

          let style: any = undefined;
          if (isActiveTrigger) style = styles.triggerHighlight;
          else if (isActiveReading) style = styles.wordBorderHighlight;

          return (
            <Text key={index} style={style}>
              {word}
              {index !== words.length - 1 ? " " : ""}
            </Text>
          );
        })}
      </Text>
    );
  };

  /* =====================================================
     RENDER
     ===================================================== */

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  if (!book) {
    return (
      <View style={styles.center}>
        <Text>Error loading book.</Text>
      </View>
    );
  }
  if (!currentPage) {
    return (
      <View style={styles.center}>
        <Text>This book has no pages.</Text>
      </View>
    );
  }

  const totalPagesInBook =
    book?.chapters?.reduce(
      (total: number, chapter: any) => total + chapter.pages.length,
      0
    ) || 0;
  const currentPageInBook =
    (book?.chapters
      ?.slice(0, currentChapterIndex)
      .reduce(
        (total: number, chapter: any) => total + chapter.pages.length,
        0
      ) || 0) +
      currentPageIndex +
      1 || 0;
  const readingProgress =
    totalPagesInBook > 0 ? currentPageInBook / totalPagesInBook : 0;

  return (
    <>
      <View style={styles.progressContainer}>
        <ProgressBar
          progress={readingProgress}
          color="#5b4636"
          style={styles.progressBar}
        />
      </View>

      <View style={styles.container}>
        <TouchableOpacity
          style={styles.topTapZone}
          onPress={openOptions}
          activeOpacity={1}
        />
        <TouchableOpacity
          style={styles.leftTouchable}
          onPress={goToPreviousPage}
          activeOpacity={1}
        />
        <TouchableOpacity
          style={styles.rightTouchable}
          onPress={goToNextPage}
          activeOpacity={1}
        />

        <View style={styles.pageCard}>
          <Text style={styles.chapterTitle}>
            {currentChapter?.title
              ? `Chapter: ${currentChapter.title}`
              : `Chapter ${currentChapter?.chapter_number}`}
          </Text>
          {renderTextWithHighlights(paginatedChunks[currentChunkIndex] || "")}
        </View>

        <Text style={styles.progressText}>
          {currentPageInBook} of {totalPagesInBook} pages
        </Text>

        {/* Backdrop */}
        {optionsOpen && (
          <TouchableOpacity
            activeOpacity={1}
            onPress={closeOptions}
            style={styles.backdrop}
          />
        )}

        {/* Panel mounts after first open to avoid initial flash */}
        {(optionsOpen || hasShownPanel) && (
          <Animated.View
            onLayout={(e) => {
              const h = e.nativeEvent.layout.height;
              setOptionsHeight(h);
              if (!hasMeasuredRef.current) {
                const closedY = -(h + insets.top + CLOSED_EXTRA);
                translateY.value = closedY; // start closed
                openProg.value = 0;
                hasMeasuredRef.current = true;
              }
            }}
            style={[styles.optionsPanel, { top: insets.top }, optionsAnim]}
          >
            <Text style={styles.panelTitle}>Options</Text>

            {/* WPM */}
            <Text style={styles.sliderTitle}>Reading speed</Text>
            <Text style={styles.sliderValue}>{wpm} wpm</Text>
            <CrossPlatformSlider
              minimumValue={50}
              maximumValue={600}
              step={10}
              value={wpm}
              onValueChange={(v: number) => {
                setWpm(v);
                save(STORAGE_KEYS.wpm, v);
              }}
              minimumTrackTintColor={COLORS.accent}
              maximumTrackTintColor="rgba(255,255,255,0.2)"
              thumbTintColor={COLORS.accent}
            />
            <View style={styles.sliderScale}>
              <Text style={styles.scaleText}>50</Text>
              <Text style={styles.scaleText}>600</Text>
            </View>
            <Text style={styles.sliderHint}>
              Tip: 180–250 wpm is comfy for most people.
            </Text>

            {/* Ambience Volume */}
            <Text style={styles.sliderTitle}>Ambience volume</Text>
            <Text style={styles.sliderValue}>{ambienceVolPct}%</Text>
            <CrossPlatformSlider
              minimumValue={0}
              maximumValue={100}
              step={1}
              value={ambienceVolPct}
              onValueChange={(v: number) => {
                setAmbienceVolPct(v);
                SoundManager.setCarpetVolume(v / 100);
                save(STORAGE_KEYS.ambVol, v);
              }}
              minimumTrackTintColor={COLORS.accent}
              maximumTrackTintColor="rgba(255,255,255,0.2)"
              thumbTintColor={COLORS.accent}
            />
            <View style={styles.sliderScale}>
              <Text style={styles.scaleText}>0</Text>
              <Text style={styles.scaleText}>100</Text>
            </View>
            <Text style={styles.sliderHint}>
              Controls the background ambience (loops).
            </Text>

            {/* Trigger Volume */}
            <Text style={styles.sliderTitle}>Trigger volume</Text>
            <Text style={styles.sliderValue}>{triggerVolPct}%</Text>
            <CrossPlatformSlider
              minimumValue={0}
              maximumValue={100}
              step={1}
              value={triggerVolPct}
              onValueChange={(v: number) => {
                setTriggerVolPct(v);
                SoundManager.setTriggerVolume(v / 100);
                save(STORAGE_KEYS.trigVol, v);
              }}
              minimumTrackTintColor={COLORS.accent}
              maximumTrackTintColor="rgba(255,255,255,0.2)"
              thumbTintColor={COLORS.accent}
            />
            <View style={styles.sliderScale}>
              <Text style={styles.scaleText}>0</Text>
              <Text style={styles.scaleText}>100</Text>
            </View>
            <Text style={styles.sliderHint}>
              Controls one‑shot sound effects on trigger words.
            </Text>

            <TouchableOpacity
              onPress={() => {
                setOptionsOpen(false);
                router.replace("/library");
              }}
              style={styles.primaryBtn}
            >
              <Text style={styles.primaryBtnText}>Back to Library</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={closeOptions}>
              <Text style={styles.closeLink}>Close</Text>
            </TouchableOpacity>
          </Animated.View>
        )}
      </View>
    </>
  );
}

/* =====================================================
   STYLES (unchanged)
   ===================================================== */

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, paddingTop: 0, position: "relative" },
  leftTouchable: {
    position: "absolute",
    top: "20%",
    left: 0,
    bottom: 0,
    width: "40%",
    zIndex: 10,
  },
  rightTouchable: {
    position: "absolute",
    top: "20%",
    right: 0,
    bottom: 0,
    width: "40%",
    zIndex: 10,
  },

  /* keep progress styles unchanged */
  progressContainer: { marginBottom: 0, zIndex: 1 },
  progressBar: { height: 2, backgroundColor: "transparent" },
  progressText: { color: "#5b4636", fontSize: 12, textAlign: "center" },

  pageCard: { flex: 1, backgroundColor: "transparent", marginBottom: 16 },
  chapterTitle: {
    marginTop: 16,
    fontWeight: "bold",
    fontSize: 18,
    color: "#5b4636",
    marginBottom: 8,
  },
  pageText: {
    fontSize: 16,
    color: "#5b4636",
    lineHeight: 24,
    textAlign: "justify",
    flexWrap: "wrap",
    flexDirection: "row",
  } as any,
  center: { flex: 1, justifyContent: "center", alignItems: "center" },

  triggerHighlight: {
    backgroundColor: "#ff6b6b",
    color: "#fff",
    padding: 2,
    borderRadius: 4,
  },
  wordBorderHighlight: { textDecorationLine: "underline", padding: 2 },
  topTapZone: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: "20%",
    zIndex: 20,
  },

  backdrop: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.45)",
    zIndex: 40,
  },

  optionsPanel: {
    position: "absolute",
    left: 12,
    right: 12,
    backgroundColor: COLORS.card,
    padding: 16,
    zIndex: 50,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: COLORS.border,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 14 },
    shadowOpacity: 0.35,
    shadowRadius: 20,
    elevation: 10,
  },
  panelTitle: {
    fontWeight: "800",
    fontSize: 20,
    color: COLORS.text,
    marginBottom: 8,
  },
  sliderTitle: {
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 6,
    color: COLORS.text,
  },
  sliderValue: {
    fontSize: 28,
    fontWeight: "800",
    marginBottom: 10,
    color: COLORS.accent,
  },
  sliderScale: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 6,
  },
  scaleText: { color: COLORS.subtext },
  sliderHint: {
    fontSize: 12,
    color: COLORS.subtext,
    marginTop: 6,
    marginBottom: 16,
  },
  closeLink: {
    color: COLORS.accent,
    fontWeight: "600",
    marginTop: 4,
    textAlign: "center",
  },
  primaryBtn: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "transparent",
    paddingVertical: 14,
    borderWidth: 1,
    borderColor: "#fff",
    borderRadius: 50,
    marginTop: 8,
    marginBottom: 16,
  },
  primaryBtnText: {
    textAlign: "center",
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
    fontFamily: "Montserrat_700Bold",
  },
});
