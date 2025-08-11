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
const { height, width } = Dimensions.get("window");
const API_HOST =
  Platform.OS === "android"
    ? "http://10.0.2.2:8000" // Android emulator -> host machine
    : "http://127.0.0.1:8000"; // iOS sim / mac

const API_BASE = `${API_HOST}/soundscape`;

type SoundscapeResponse = {
  book_id: number;
  book_page_id: number;
  summary: string;
  detected_scenes: string[];
  scene_keyword_counts: Record<string, number>;
  scene_keyword_positions: Record<string, number[]>;
  carpet_tracks: string[]; // e.g. ["windy_mountains.mp3"]
  triggered_sounds: Array<{ word: string; position: number; file: string }>;
};

async function fetchSoundscape(
  bookId: string | number,
  chapterNumber: number,
  pageNumber: number
): Promise<SoundscapeResponse> {
  console.log(
    `Fetching soundscape: ${API_BASE}/book/${bookId}/chapter${chapterNumber}/page/${pageNumber}`
  );
  const res = await fetch(
    `${API_BASE}/book/${bookId}/chapter${chapterNumber}/page/${pageNumber}`
  );
  if (!res.ok) {
    throw new Error(`soundscape ${res.status}`);
  }
  return res.json();
}

export default function BookDetailScreen() {
  const params = useLocalSearchParams();
  const router = useRouter();

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

  const { wpm, setWpm } = useWpm();

  const wpmRef = React.useRef(wpm);
  React.useEffect(() => {
    wpmRef.current = wpm;
  }, [wpm]);

  const currentWordIndexRef = React.useRef(0);
  React.useEffect(() => {
    if (activeWordIndex != null) currentWordIndexRef.current = activeWordIndex;
  }, [activeWordIndex]);

  const firedTriggerIdsRef = React.useRef<Set<string>>(new Set());
  type TimeoutId = ReturnType<typeof setTimeout>;
  const wordTimeoutRef = React.useRef<TimeoutId | null>(null);

  const { bookId } = params;
  const { book, loading } = useBook(bookId as string) as {
    book: any;
    loading: boolean;
  };

  const [optionsOpen, setOptionsOpen] = React.useState(false);
  const translateY = useSharedValue(-200);
  const optionsAnim = useAnimatedStyle(() => ({
    transform: [
      { translateY: withTiming(translateY.value, { duration: 250 }) },
    ],
  }));
  React.useEffect(() => {
    translateY.value = optionsOpen ? 0 : -300;
  }, [optionsOpen, translateY]);

  React.useEffect(() => {
    router.setParams({
      chapter: String(currentChapterIndex),
      page: String(currentPageIndex),
      chunk: String(currentChunkIndex),
    });
  }, [currentChapterIndex, currentPageIndex, currentChunkIndex]);

  React.useEffect(() => {
    if (params.chapter !== undefined)
      setCurrentChapterIndex(Number(params.chapter));
    if (params.page !== undefined) setCurrentPageIndex(Number(params.page));
    if (params.chunk !== undefined) setCurrentChunkIndex(Number(params.chunk));
  }, [params.chapter, params.page, params.chunk]);

  const paginateText = (text: string, fontSize = 16, lineHeight = 24) => {
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
  };

  const calculateWordTiming = (text: string) => {
    if (!text) return { words: [], msPerWord: 333 };
    const words = text.split(/\s+/).filter(Boolean);
    const msPerWord = 60000 / (wpmRef.current || 200);
    return { words, msPerWord };
  };

  const findTriggerWords = (text: string) => {
    const { words, msPerWord } = calculateWordTiming(text);
    return words
      .map((word, index) => {
        const clean = word.toLowerCase().replace(/[^\w]/g, "");
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
      .filter(Boolean) as TriggerWord[];
  };

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

      const sourceTriggers = triggersArg ?? triggerWords;
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

          // prefer API-provided sound file; fall back to word mapping
          const assetKey = trig.soundKey ?? trig.word;
          const asset = SOUND_MAP[assetKey] ?? WORD_TRIGGERS[trig.word];

          if (asset) {
            SoundManager.playTrigger(asset).finally(() => {
              setActiveTriggerWords((prev) => {
                const s = new Set(prev);
                s.delete(trig.id);
                return s;
              });
            });
          } else {
            // no asset mapped; clear highlight anyway
            setActiveTriggerWords((prev) => {
              const s = new Set(prev);
              s.delete(trig.id);
              return s;
            });
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
    [paginatedChunks, currentChunkIndex, triggerWords, stopReadingTimer]
  );

  const openOptions = React.useCallback(() => {
    stopReadingTimer();
    setOptionsOpen(true);
  }, [stopReadingTimer]);

  const closeOptions = React.useCallback(() => {
    setOptionsOpen(false);
    startReadingTimer(currentWordIndexRef.current ?? 0);
  }, [startReadingTimer]);

  const currentChapter = book?.chapters?.[currentChapterIndex];
  const currentPage = currentChapter?.pages?.[currentPageIndex];
  const totalChapters = book?.chapters?.length || 0;
  const totalPages = currentChapter?.pages?.length || 0;

  const goToNextPage = () => {
    stopReadingTimer();
    if (currentChunkIndex < paginatedChunks.length - 1) {
      setCurrentChunkIndex(currentChunkIndex + 1);
      return;
    }
    if (currentPageIndex < totalPages - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
      setCurrentChunkIndex(0);
    } else if (currentChapterIndex < totalChapters - 1) {
      setCurrentChapterIndex(currentChapterIndex + 1);
      setCurrentPageIndex(0);
      setCurrentChunkIndex(0);
    }
  };

  const goToPreviousPage = () => {
    stopReadingTimer();
    if (
      currentChapterIndex === 0 &&
      currentPageIndex === 0 &&
      currentChunkIndex === 0
    ) {
      router.replace("/library");
      return;
    }
    if (currentChunkIndex > 0) {
      setCurrentChunkIndex(currentChunkIndex - 1);
      return;
    }
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
      setCurrentChunkIndex(0);
    } else if (currentChapterIndex > 0) {
      const prevChapter = book?.chapters?.[currentChapterIndex - 1];
      const lastPageIndex = (prevChapter?.pages?.length || 1) - 1;
      setCurrentChapterIndex(currentChapterIndex - 1);
      setCurrentPageIndex(lastPageIndex);
      setCurrentChunkIndex(0);
    }
  };

  // helper: map API "sound" path to a key you actually have in SOUND_MAP
  function resolveSoundKey(soundFromApi?: string): string | undefined {
    if (!soundFromApi) return undefined;

    // Quick exact hit
    if (SOUND_MAP[soundFromApi]) return soundFromApi;

    // Split into folder(s) + base
    const parts = soundFromApi.split("/");
    const baseRaw = parts.pop() || soundFromApi; // e.g. "default_ambience" or "windy_mountains.mp3"
    const folders = parts.length ? parts : []; // e.g. ["ambience"]
    const baseNoExt = baseRaw.replace(/\.[^/.]+$/, ""); // strip ext if present
    const exts = [".mp3", ".m4a", ".wav", ".ogg"];

    // Candidate keys to try in SOUND_MAP, most specific first
    const candidates: string[] = [];

    // 1) same folder + with/without ext
    for (const dir of [...folders, "ambience", "triggers", ""]) {
      const prefix = dir ? `${dir}/` : "";
      candidates.push(`${prefix}${baseRaw}`);
      candidates.push(`${prefix}${baseNoExt}`);
      for (const ext of exts) candidates.push(`${prefix}${baseNoExt}${ext}`);
    }

    // 2) Try simple filename only (with common extensions)
    candidates.push(baseNoExt);
    for (const ext of exts) candidates.push(`${baseNoExt}${ext}`);

    // Return the first candidate that exists in the map
    for (const c of candidates) {
      if (SOUND_MAP[c]) return c;
    }

    // 3) Fuzzy: look for any key containing or ending with the stem
    const keys = Object.keys(SOUND_MAP);
    const fuzzy = keys.find(
      (k) =>
        k.endsWith(`/${baseNoExt}`) ||
        k.endsWith(`${baseNoExt}`) ||
        k.endsWith(`${baseNoExt}.mp3`) ||
        k.includes(`/${baseNoExt}.`)
    );
    if (fuzzy) return fuzzy;

    // 4) Last resort heuristics (optional)
    if (/thunder/i.test(soundFromApi))
      return "triggers/thunder-city-377703.mp3";
    if (/footstep/i.test(soundFromApi))
      return "triggers/footsteps-approaching-316715.mp3";
    if (/wind/i.test(soundFromApi)) return "triggers/wind.mp3";
    if (/storm/i.test(soundFromApi)) return "triggers/storm.mp3";

    // 5) Hard fallback to your default ambience if present
    if (SOUND_MAP["ambience/default_ambience.mp3"])
      return "ambience/default_ambience.mp3";

    return undefined;
  }

  // Normalize a token the same way everywhere
  function norm(w: string) {
    return w.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ""); // letters+digits, Unicode-safe
  }

  // Split text into tokens (client-side reference tokenization)
  function tokenize(text: string) {
    return text.split(/\s+/).filter(Boolean);
  }

  // Find the nearest token index around an approximate position whose normalized form matches target
  function snapToNearestToken(
    tokens: string[],
    targetWord: string,
    approxIdx: number,
    window = 2
  ) {
    const target = norm(targetWord);
    // exact hit first
    if (tokens[approxIdx] && norm(tokens[approxIdx]) === target)
      return approxIdx;

    // search a small window around the guess to correct off-by-one/two
    for (let delta = 1; delta <= window; delta++) {
      const left = approxIdx - delta;
      const right = approxIdx + delta;
      if (left >= 0 && norm(tokens[left] || "") === target) return left;
      if (right < tokens.length && norm(tokens[right] || "") === target)
        return right;
    }
    return approxIdx; // fallback: leave as-is
  }

  const loadSoundscapeForPage = async (
    chapterIndex?: number,
    pageIndex?: number
  ) => {
    if (!book) return;

    const ci = chapterIndex ?? currentChapterIndex;
    const pi = pageIndex ?? currentPageIndex;

    // ✅ real numbers from your book JSON (fallback to index+1 if missing)
    const chapterNumber = book.chapters?.[ci]?.chapter_number ?? ci + 1;
    const pageNumber = book.chapters?.[ci]?.pages?.[pi]?.page_number ?? pi + 1;

    console.log("📡 Sending to API:", {
      bookId,
      chapterNumber,
      pageNumber,
      ci,
      pi,
    });

    try {
      const data = await fetchSoundscape(
        bookId as string,
        chapterNumber,
        pageNumber
      );

      // how many words come BEFORE the current chunk? (to shift absolute → chunk positions)
      const chunkText = paginatedChunks[currentChunkIndex] || "";
      const chunkTokens = tokenize(chunkText);

      // how many words before this chunk (so we can convert absolute -> chunk index)
      const wordsBeforeThisChunk = paginatedChunks
        .slice(0, currentChunkIndex)
        .reduce((sum, ch) => sum + tokenize(ch).length, 0);

      // Map API triggers -> client triggers, then SNAP indexes
      const chunkTriggers: TriggerWord[] = (data.triggered_sounds || [])
        .map((t: any, i: number) => {
          const absolutePos = Number(t.word_position ?? t.position ?? 0);
          const approxInChunk = absolutePos - wordsBeforeThisChunk;

          // snap to the nearest real token that matches "storm", "wind", etc.
          const snapped = snapToNearestToken(
            chunkTokens,
            String(t.word || ""),
            approxInChunk,
            2
          );

          console.log(
            "🔑 SOUND_MAP contains:",
            Object.keys(SOUND_MAP).filter((k) => k.includes("environmental"))
          );

          return {
            id: String(i),
            word: String(t.word || "").toLowerCase(),
            position: snapped,
            timing: 0,
            soundKey: resolveSoundKey(t.sound), // keep your resolver
          };
        })
        .filter((t) => t.position >= 0 && t.position < chunkTokens.length);

      // swap in server triggers + restart reader using them
      setTriggerWords(chunkTriggers);
      stopReadingTimer();
      startReadingTimer(0, chunkTriggers); // make sure startReadingTimer prefers trig.soundKey if present

      // play ambient "carpet" from API (first track)
      // play ambient "carpet" from API (first track) with key resolution + logs
      const first = data.carpet_tracks?.[0];
      const resolvedCarpetKey = resolveSoundKey(first);

      console.log("🪵 Carpet from API:", { raw: first, resolvedCarpetKey });

      if (resolvedCarpetKey && SOUND_MAP[resolvedCarpetKey]) {
        try {
          console.log(
            `🎵 Playing ambient (API): "${first}" → "${resolvedCarpetKey}"`
          );
          await SoundManager.playCarpet(
            SOUND_MAP[resolvedCarpetKey],
            resolvedCarpetKey
          );
        } catch (e) {
          console.warn("❗ playCarpet failed (API):", e);
        }
      } else if (first) {
        console.warn("⚠️ No SOUND_MAP match for API carpet:", first);
      }

      return; // handled by API
    } catch (err) {
      console.log("Soundscape API fallback:", err);
    }

    // --- fallback to your local mapping if API fails ---
    const page = book?.chapters?.[ci]?.pages?.[pi];
    let ambienceKey = page?.ambient as string;

    if (!ambienceKey) {
      const pageAmbienceMap: Record<string, string> = {
        "0-0": "windy_mountains.mp3",
        "0-1": "cabin_rain.mp3",
        "1-0": "stormy_night.mp3",
      };
      ambienceKey = pageAmbienceMap[`${ci}-${pi}`] || "default_ambience.mp3";
    }

    const asset = SOUND_MAP[ambienceKey];
    console.log("🌲 Fallback ambience:", { ambienceKey, assetFound: !!asset });

    if (asset) {
      try {
        console.log(`🎵 Playing ambient (fallback): "${ambienceKey}"`);
        await SoundManager.playCarpet(asset, ambienceKey);
      } catch (e) {
        console.warn("❗ playCarpet failed (fallback):", e);
      }
    } else {
      console.warn("⚠️ No SOUND_MAP for fallback ambience:", ambienceKey);
    }
  };

  React.useEffect(() => {
    if (book && currentPage) {
      const chunks = paginateText(currentPage.content);
      setPaginatedChunks(chunks);
      setCurrentChunkIndex(0);
    }
  }, [book, currentChapterIndex, currentPageIndex]);

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
    currentChunkIndex,
    currentPageIndex,
    currentChapterIndex,
    paginatedChunks,
  ]);

  React.useEffect(() => {
    if (paginatedChunks.length > 0) {
      startReadingTimer(currentWordIndexRef.current ?? 0);
    }
  }, [wpm, startReadingTimer, paginatedChunks.length]);

  useFocusEffect(
    React.useCallback(() => {
      return () => {
        SoundManager.stopAll();
        stopReadingTimer();
      };
    }, [stopReadingTimer])
  );

  React.useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => {
      if (s === "background" || s === "inactive") {
        SoundManager.stopAll();
        stopReadingTimer();
      }
    });
    return () => sub.remove();
  }, [stopReadingTimer]);

  const renderTextWithHighlights = (text: string) => {
    const words = text.split(/\s+/).filter(Boolean);
    return (
      <Text style={styles.pageText}>
        {words.map((word, index) => {
          const clean = word.toLowerCase().replace(/[^\w]/g, "");
          const trigger = triggerWords.find((t) => t.position === index);
          const isActiveTrigger = trigger
            ? activeTriggerWords.has(trigger.id)
            : false;
          const isActiveReading = activeWordIndex === index;

          let style = undefined;
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
        <Animated.View style={[styles.optionsPanel, optionsAnim]}>
          <Text style={{ fontWeight: "bold", fontSize: 16 }}>Options</Text>
          <Text style={styles.sliderTitle}>Reading speed</Text>
          <Text style={styles.sliderValue}>{wpm} wpm</Text>
          <CrossPlatformSlider
            minimumValue={50}
            maximumValue={600}
            step={10}
            value={wpm}
            onValueChange={setWpm}
          />
          <View style={styles.sliderScale}>
            <Text>50</Text>
            <Text>600</Text>
          </View>
          <Text style={styles.sliderHint}>
            Tip: 180–250 wpm is comfy for most people.
          </Text>
          <TouchableOpacity onPress={closeOptions}>
            <Text style={{ color: "blue" }}>Close</Text>
          </TouchableOpacity>
        </Animated.View>
      </View>
    </>
  );
}

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
  progressContainer: { marginBottom: 16 },
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
  wordBorderHighlight: {
    textDecorationLine: "underline",
    padding: 2,
  },
  topTapZone: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: "20%",
    zIndex: 20,
  },
  optionsPanel: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    backgroundColor: "#fff",
    padding: 16,
    zIndex: 50,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
  sliderTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8,
    color: "#5b4636",
  },
  sliderValue: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 12,
    color: "red",
  },
  sliderScale: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 8,
  },
  sliderHint: {
    fontSize: 12,
    color: "#888",
    marginTop: 4,
    marginBottom: 16,
  },
});
