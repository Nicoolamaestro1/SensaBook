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
  ScrollView,
  Platform,
} from "react-native";
import {
  SafeAreaView,
  useSafeAreaInsets,
} from "react-native-safe-area-context";
import { ProgressBar } from "react-native-paper";
import Animated, {
  useSharedValue,
  withTiming,
  useAnimatedStyle,
} from "react-native-reanimated";
import { GestureDetector, Gesture } from "react-native-gesture-handler";
import { runOnJS } from "react-native-reanimated";
import AsyncStorage from "@react-native-async-storage/async-storage";

import SoundManager from "../utils/soundManager";
import { useBook } from "../../hooks/useBooks";
import { useWpm } from "../../hooks/useWpm";
import {
  WORD_TRIGGERS,
  TriggerWord,
  SOUND_MAP,
  resolveSoundKey,
} from "../../constants/sounds";
import {
  calculateWordTiming,
  findTriggerWords,
  fetchSoundscape,
  tokenize,
  snapToNearestToken,
  computeReadingProgress,
  paginateText,
} from "../utils/reading";
import type { Book, Chapter, Page } from "../../types/book";
import type { SoundscapeResponse } from "../../types/soundscape";
import ReadingControls from "../components/ReadingControls";
import { WordTracker } from "../components/WordTracker";

const COLORS = Object.freeze({
  card: "#17171c",
  text: "#EAEAF0",
  subtext: "#A6A8B1",
  border: "rgba(255,255,255,0.06)",
  accent: "#fff",
});
const STORAGE_KEYS = Object.freeze({
  wpm: "settings.wpm",
  ambVol: "settings.ambienceVolPct",
  trigVol: "settings.triggerVolPct",
  fontSize: "settings.fontSizePt",
});
const FONT_MIN = 12;
const FONT_MAX = 28;
const { height: SCREEN_H, width: SCREEN_W } = Dimensions.get("window");
type TimeoutId = ReturnType<typeof setTimeout>;

/* ---------- measured line model & helpers (NEW) ---------- */
type LineBox = { text: string; height: number; isSpacer?: boolean };

/** Kindle-like: paragraphs are independent blocks; blank line between paragraphs. */
function splitParagraphs(collapsed: string): string[] {
  // collapsed uses the sentinel \n¶\n between paragraphs; keep it robust too
  return collapsed
    .replace(/\r/g, "")
    .split(/\n¶\n|(?:\n\s*\n+)/g)
    .map((p) => p.trim())
    .filter(Boolean);
}

/** Pack measured line boxes up to the page height (pixel-precise). */
function paginateByLineBoxesPx(lines: LineBox[], pageHeight: number): string[] {
  if (pageHeight <= 0 || !lines.length)
    return [lines.map((l) => l.text).join("\n")];

  const EPS = 0.5; // avoid 1px rounding nudges
  const pages: string[] = [];
  let i = 0;

  while (i < lines.length) {
    const start = i;
    let used = 0;

    // fill while it fits
    while (i < lines.length && used + lines[i].height <= pageHeight - EPS) {
      used += lines[i].height;
      i++;
    }

    // always emit at least one line per page
    if (i === start) i++;

    pages.push(
      lines
        .slice(start, i)
        .map((l) => l.text)
        .join("\n")
    );
  }
  return pages;
}

export default function BookDetailScreen() {
  const params = useLocalSearchParams();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  // panel animation
  const CLOSED_EXTRA = 40;
  const translateY = useSharedValue(-10000);
  const openProg = useSharedValue(0);
  const hasMeasuredRef = React.useRef(false);

  // layout + pagination
  const [containerWidth, setContainerWidth] = React.useState(0);
  const [containerHeight, setContainerHeight] = React.useState(0);
  const [measuredBoxes, setMeasuredBoxes] = React.useState<LineBox[]>([]);
  const [paginatedChunks, setPaginatedChunks] = React.useState<string[]>([]);

  // ui
  const [optionsOpen, setOptionsOpen] = React.useState(false);
  const [hasShownPanel, setHasShownPanel] = React.useState(false);
  const [optionsHeight, setOptionsHeight] = React.useState(0);

  // location within book
  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(
    Number(params.chapter ?? 0)
  );
  const [currentPageIndex, setCurrentPageIndex] = React.useState(
    Number(params.page ?? 0)
  );
  const [currentChunkIndex, setCurrentChunkIndex] = React.useState(
    Number(params.chunk ?? 0)
  );

  // reading state
  const [triggerWords, setTriggerWords] = React.useState<TriggerWord[]>([]);
  const [activeTriggerWords, setActiveTriggerWords] = React.useState<
    Set<string>
  >(new Set());
  const [activeWordIndex, setActiveWordIndex] = React.useState<number | null>(
    null
  );

  // volumes + wpm + font
  const [ambienceVolPct, setAmbienceVolPct] = React.useState(60);
  const [triggerVolPct, setTriggerVolPct] = React.useState(80);
  const [fontSize, setFontSize] = React.useState<number>(16);
  const { wpm, setWpm } = useWpm();

  // type metrics
  const lineHeight = Math.max(Math.round(fontSize * 1.5), fontSize + 6);
  const titleFontSize = Math.round(fontSize * 1.125);
  const titleLineHeight = Math.round(titleFontSize * 1.35);

  // word-tracker state
  const [chunkWordCount, setChunkWordCount] = React.useState(0);
  const [triggerPositions, setTriggerPositions] = React.useState<Set<number>>(
    new Set()
  );
  const [trackerMarks, setTrackerMarks] = React.useState<number[]>([]);
  const [seekingIndex, setSeekingIndex] = React.useState<number | null>(null);

  // refs
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
  const wordTimeoutRef = React.useRef<TimeoutId | null>(null);

  // data
  const { bookId } = params;
  const { book, loading } = useBook(bookId as string) as {
    book: Book | null;
    loading: boolean;
  };
  const currentChapter: Chapter | undefined =
    book?.chapters?.[currentChapterIndex];
  const currentPage: Page | undefined =
    currentChapter?.pages?.[currentPageIndex];

  // panel anim
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

  // persist settings
  React.useEffect(() => {
    (async () => {
      try {
        const [w, a, t, f] = await Promise.all([
          AsyncStorage.getItem(STORAGE_KEYS.wpm),
          AsyncStorage.getItem(STORAGE_KEYS.ambVol),
          AsyncStorage.getItem(STORAGE_KEYS.trigVol),
          AsyncStorage.getItem(STORAGE_KEYS.fontSize),
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
        if (f) {
          const n = clampFont(Number(f));
          setFontSize(n);
        }
      } catch {}
    })();
  }, [setWpm]);
  const save = React.useCallback(
    (key: string, value: number | string) =>
      AsyncStorage.setItem(key, String(value)).catch(() => {}),
    []
  );

  // url sync
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

  // timers
  const stopReadingTimer = React.useCallback(() => {
    if (wordTimeoutRef.current) {
      clearTimeout(wordTimeoutRef.current);
      wordTimeoutRef.current = null;
    }
  }, []);
  const getCurrentChunkText = React.useCallback(
    () => paginatedChunks[currentChunkIndex] || "",
    [paginatedChunks, currentChunkIndex]
  );

  // Recompute word count for current chunk  // NEW
  // Recompute word count for the current chunk  (NEW)
  React.useEffect(() => {
    const text = getCurrentChunkText();
    const words = text.split(/\s+/).filter(Boolean);
    setChunkWordCount(words.length);
  }, [getCurrentChunkText, currentChunkIndex, paginatedChunks]);

  // Fast lookup set of trigger positions within the chunk  (NEW)
  React.useEffect(() => {
    setTriggerPositions(new Set(triggerWords.map((t) => t.position)));
  }, [triggerWords]);

  // Normalized tick marks for the tracker [0..1]  (NEW)
  React.useEffect(() => {
    const denom = Math.max(1, chunkWordCount - 1);
    setTrackerMarks(
      Array.from(triggerPositions).map((p) =>
        Math.min(1, Math.max(0, p / denom))
      )
    );
  }, [triggerPositions, chunkWordCount]);

  // Reset seeking overlay when page/chunk changes  (NEW)
  React.useEffect(() => {
    setSeekingIndex(null);
  }, [currentChunkIndex]);
  const startReadingTimer = React.useCallback(
    (resumeFromIndex?: number, triggersArg?: TriggerWord[]) => {
      stopReadingTimer();
      const chunk = getCurrentChunkText();
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
          const assetKey = trig.soundKey ?? trig.word;
          if (
            typeof assetKey === "string" &&
            assetKey.startsWith("ambience/")
          ) {
            setActiveTriggerWords((prev) => {
              const s = new Set(prev);
              s.delete(trig.id);
              return s;
            });
          } else {
            const asset = SOUND_MAP[assetKey] ?? WORD_TRIGGERS[trig.word];
            if (asset) {
              SoundManager.playTrigger(asset).finally(() =>
                setActiveTriggerWords((prev) => {
                  const s = new Set(prev);
                  s.delete(trig.id);
                  return s;
                })
              );
            } else {
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
        if (idx < words.length)
          wordTimeoutRef.current = setTimeout(tick, msPerWord);
        else stopReadingTimer();
      };
      wordTimeoutRef.current = setTimeout(tick, msPerWord);
    },
    [getCurrentChunkText, stopReadingTimer]
  );

  const [lastCarpet, setLastCarpet] = React.useState<{
    key?: string;
    asset?: number;
  } | null>(null);
  const ensureAmbienceAfterGesture = React.useCallback(() => {
    if (lastCarpet?.asset)
      SoundManager.playCarpet(lastCarpet.asset, lastCarpet.key);
  }, [lastCarpet]);

  // options
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

  // nav
  const pageCount = paginatedChunks.length;
  const { book: __b } = { book }; // silence unused warning

  const goToNextPage = React.useCallback(() => {
    stopReadingTimer();
    SoundManager.stopTriggers(500);
    ensureAmbienceAfterGesture();
    if (currentChunkIndex < Math.max(0, pageCount - 1)) {
      setCurrentChunkIndex((i) => i + 1);
      return;
    }
    if (currentPageIndex < (currentChapter?.pages?.length || 0) - 1) {
      setCurrentPageIndex((i) => i + 1);
      setCurrentChunkIndex(0);
    } else if ((book?.chapters?.length || 0) - 1 > currentChapterIndex) {
      setCurrentChapterIndex((i) => i + 1);
      setCurrentPageIndex(0);
      setCurrentChunkIndex(0);
    }
  }, [
    stopReadingTimer,
    ensureAmbienceAfterGesture,
    currentChunkIndex,
    pageCount,
    currentPageIndex,
    currentChapter?.pages?.length,
    currentChapterIndex,
    book?.chapters?.length,
  ]);

  const goToPreviousPage = React.useCallback(() => {
    stopReadingTimer();
    SoundManager.stopTriggers(500);
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
      const prev = book?.chapters?.[currentChapterIndex - 1];
      const lastIdx = (prev?.pages?.length || 1) - 1;
      setCurrentChapterIndex((i) => i - 1);
      setCurrentPageIndex(lastIdx);
      setCurrentChunkIndex(0);
    }
  }, [
    stopReadingTimer,
    ensureAmbienceAfterGesture,
    currentChapterIndex,
    currentPageIndex,
    currentChunkIndex,
    router,
    book?.chapters,
  ]);

  // --- tracker seek handlers (NEW) ---
  const onSeekStart = React.useCallback(() => {
    stopReadingTimer();
    setSeekingIndex(activeWordIndex ?? 0);
    setActiveTriggerWords(new Set());
  }, [stopReadingTimer, activeWordIndex]);

  const onSeekPreview = React.useCallback((idx: number) => {
    setSeekingIndex(idx);
  }, []);

  const onSeekEnd = React.useCallback(
    (idx: number) => {
      setSeekingIndex(null);
      // jump and resume from selected word
      startReadingTimer(Math.max(0, Math.min(idx, (chunkWordCount || 1) - 1)));
    },
    [startReadingTimer, chunkWordCount]
  );

  const swipe = React.useMemo(() => {
    return Gesture.Pan()
      .onEnd((e) => {
        const { translationX, translationY } = e;
        if (Math.abs(translationX) > Math.abs(translationY)) {
          if (translationX > 0) runOnJS(goToPreviousPage)();
          else runOnJS(goToNextPage)();
        } else {
          if (translationY > 0) runOnJS(openOptions)();
          else runOnJS(closeOptions)();
        }
      })
      .enabled(!optionsOpen);
  }, [optionsOpen, goToNextPage, goToPreviousPage, openOptions, closeOptions]);

  // soundscape
  const loadSoundscapeForPage = React.useCallback(
    async (chapterIndex?: number, pageIndex?: number) => {
      if (!book) return;
      const ci = chapterIndex ?? currentChapterIndex;
      const pi = pageIndex ?? currentPageIndex;
      const chapterNumber = book.chapters?.[ci]?.chapter_number ?? ci + 1;
      const pageNumber =
        book.chapters?.[ci]?.pages?.[pi]?.page_number ?? pi + 1;

      try {
        const data: SoundscapeResponse = await fetchSoundscape(
          Number(bookId),
          chapterNumber,
          pageNumber
        );
        const chunkText = getCurrentChunkText();
        const chunkTokens = tokenize(chunkText);
        const wordsBeforeThisChunk = paginatedChunks
          .slice(0, currentChunkIndex)
          .reduce((sum, ch) => sum + tokenize(ch).length, 0);

        const chunkTriggers: TriggerWord[] = (data.triggered_sounds ?? [])
          .map((t, i: number) => {
            const absolutePos = Number(
              (t as any).word_position ?? t.position ?? 0
            );
            const approxInChunk = absolutePos - wordsBeforeThisChunk;
            const snapped = snapToNearestToken(
              chunkTokens,
              String((t as any).word || ""),
              approxInChunk,
              2
            );
            const rawKey = resolveSoundKey((t as any).sound ?? (t as any).file);
            const safeKey =
              rawKey && rawKey.startsWith("ambience/") ? undefined : rawKey;
            return {
              id: String(i),
              word: String((t as any).word || "").toLowerCase(),
              position: snapped,
              timing: 0,
              soundKey: safeKey,
            } as TriggerWord;
          })
          .filter((tw) => tw.position >= 0 && tw.position < chunkTokens.length);

        setTriggerWords(chunkTriggers);
        stopReadingTimer();
        startReadingTimer(0, chunkTriggers);

        const first = (data.carpet_tracks ?? [])[0];
        const resolved = resolveSoundKey(first);
        if (resolved && SOUND_MAP[resolved]) {
          const asset = SOUND_MAP[resolved];
          setLastCarpet({ key: resolved, asset });
          await SoundManager.playCarpet(asset, resolved);
        }
      } catch {
        const page = book?.chapters?.[ci]?.pages?.[pi];
        let ambienceKey =
          (page?.ambient as string | undefined) ||
          "ambience/default_ambience.mp3";
        const pageAmbienceMap: Record<string, string> = {
          "0-0": "ambience/windy_mountains.mp3",
          "0-1": "ambience/cabin_rain.mp3",
          "1-0": "ambience/stormy_night.mp3",
        };
        ambienceKey =
          page?.ambient || pageAmbienceMap[`${ci}-${pi}`] || ambienceKey;
        const asset = SOUND_MAP[ambienceKey];
        if (asset) {
          setLastCarpet({ key: ambienceKey, asset });
          await SoundManager.playCarpet(asset, ambienceKey);
        }
      }
    },
    [
      book,
      bookId,
      currentChapterIndex,
      currentPageIndex,
      currentChunkIndex,
      paginatedChunks,
      getCurrentChunkText,
      startReadingTimer,
      stopReadingTimer,
    ]
  );

  // lifecycle
  React.useEffect(
    () => () => {
      SoundManager.stopCarpet();
    },
    [bookId]
  );

  /* ------------------------- TEXT NORMALIZATION ------------------------- */
  const fullTextRaw =
    book?.chapters?.[currentChapterIndex]?.pages?.[currentPageIndex]?.content ??
    "";

  // Collapse multiple blank lines to a sentinel we can split on
  const collapsedFullText = React.useMemo(
    () => fullTextRaw.replace(/[ \t]*(?:\r?\n)+/g, "\n¶\n"),
    [fullTextRaw]
  );

  // For WEB rendering only (native ignores this in favor of measured boxes)
  const GAP_JOINER = Platform.select({
    ios: "\n\n", // exactly one blank line on iOS
    android: "\n\u00A0", // one visible/measurable blank line on Android
    default: "\n\u00A0",
  });
  const normalizedText = React.useMemo(
    () => collapsedFullText.split("\n¶\n").join(GAP_JOINER),
    [collapsedFullText, GAP_JOINER]
  );

  // Paragraph list for the native measurer
  const paragraphs = React.useMemo(
    () => splitParagraphs(collapsedFullText),
    [collapsedFullText]
  );

  /* ------------------------- PAGINATION ------------------------- */

  // reset measurements when text metrics or page changes
  React.useEffect(() => {
    setMeasuredBoxes([]);
  }, [currentChapterIndex, currentPageIndex, fontSize]);

  // WEB pagination (unchanged heuristic)
  React.useEffect(() => {
    if (!currentPage) return;
    if (Platform.OS !== "web") return;
    const chunks = paginateText(
      normalizedText,
      {
        width: containerWidth || SCREEN_W,
        height: containerHeight || SCREEN_H,
      },
      { fontSize, lineHeight }
    );
    setPaginatedChunks(chunks);
    setCurrentChunkIndex(0);
  }, [
    currentPage,
    containerWidth,
    containerHeight,
    fontSize,
    lineHeight,
    normalizedText,
  ]);

  // NATIVE pagination — pixel-precise using measured line heights
  React.useEffect(() => {
    if (
      Platform.OS === "web" ||
      !currentPage ||
      !containerWidth ||
      !containerHeight ||
      !measuredBoxes.length
    )
      return;
    const pages = paginateByLineBoxesPx(measuredBoxes, containerHeight);
    setPaginatedChunks(pages);
    setCurrentChunkIndex((idx) => Math.min(idx, Math.max(0, pages.length - 1)));
  }, [currentPage, measuredBoxes, containerWidth, containerHeight]);

  // reset to first chunk on chapter/page/font change
  React.useEffect(() => {
    setCurrentChunkIndex(0);
  }, [currentChapterIndex, currentPageIndex, fontSize]);

  // when page changes, compute triggers & start timer & soundscape
  React.useEffect(() => {
    if (!book || !currentPage || paginatedChunks.length === 0) return;
    const chunk = getCurrentChunkText();
    if (!chunk) return;
    const { words, msPerWord } = calculateWordTiming(
      chunk,
      wpmRef.current || 200
    );
    const triggers = findTriggerWords(words, msPerWord);
    setTriggerWords(triggers);
    setActiveTriggerWords(new Set());
    setActiveWordIndex(0);
    loadSoundscapeForPage(currentChapterIndex, currentPageIndex);
    startReadingTimer(0, triggers);
  }, [
    book,
    currentChapterIndex,
    currentPageIndex,
    currentChunkIndex,
    paginatedChunks,
    getCurrentChunkText,
    loadSoundscapeForPage,
    startReadingTimer,
  ]);

  React.useEffect(() => {
    if (paginatedChunks.length > 0)
      startReadingTimer(currentWordIndexRef.current ?? 0);
  }, [wpm, startReadingTimer, paginatedChunks.length]);

  useFocusEffect(
    React.useCallback(
      () => () => {
        SoundManager.stopTriggers(250);
        SoundManager.stopCarpet(300);
        stopReadingTimer();
      },
      [stopReadingTimer]
    )
  );

  React.useEffect(() => {
    SoundManager.setCarpetVolume(ambienceVolPct / 100);
    SoundManager.setTriggerVolume(triggerVolPct / 100);
  }, []);
  React.useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => {
      if (s === "background" || s === "inactive") {
        SoundManager.stopTriggers(250);
        SoundManager.stopCarpet(300);
        stopReadingTimer();
      }
    });
    return () => sub.remove();
  }, [stopReadingTimer]);

  // guards
  if (loading)
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  if (!book)
    return (
      <View style={styles.center}>
        <Text>Error loading book.</Text>
      </View>
    );
  if (!currentPage)
    return (
      <View style={styles.center}>
        <Text>This book has no pages.</Text>
      </View>
    );

  const {
    totalPagesInBook,
    currentPageInBook,
    progress: readingProgress,
  } = computeReadingProgress(book, currentChapterIndex, currentPageIndex);

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={styles.progressContainer}>
        <ProgressBar
          progress={readingProgress}
          color="#1F190F"
          style={styles.progressBar}
        />
      </View>

      <View style={[styles.container, { paddingTop: insets.top }]}>
        {/* Swipe ONLY over the reading area */}
        <GestureDetector gesture={swipe}>
          <View style={{ flex: 1 }}>
            {!optionsOpen && (
              <>
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
              </>
            )}

            <View
              style={styles.pageCard}
              onLayout={(e) => setContainerWidth(e.nativeEvent.layout.width)}
            >
              <View>
                <Text
                  style={[
                    styles.chapterTitle,
                    { fontSize: titleFontSize, lineHeight: titleLineHeight },
                  ]}
                >
                  {currentChapter?.title
                    ? `Chapter: ${currentChapter.title}`
                    : `Chapter ${currentChapter?.chapter_number}`}
                </Text>
              </View>

              <View
                style={styles.bodyWrapper}
                onLayout={(e) => {
                  const { width: w, height: h } = e.nativeEvent.layout;
                  setContainerWidth(w);
                  setContainerHeight(h);
                }}
              >
                {/* Invisible measurer */}
                {Platform.OS !== "web" && containerWidth > 0 && (
                  <View
                    collapsable={false}
                    pointerEvents="none"
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      width: containerWidth,
                      opacity: 0,
                    }}
                  >
                    <ParagraphMeasurer
                      paragraphs={paragraphs}
                      fontSize={fontSize}
                      lineHeight={lineHeight}
                      width={containerWidth}
                      onMeasured={setMeasuredBoxes}
                    />
                  </View>
                )}

                {/* Visible chunk */}
                <Text
                  style={[styles.pageText, { fontSize, lineHeight }]}
                  allowFontScaling={false}
                  {...Platform.select({
                    android: { textBreakStrategy: "highQuality" as const },
                    default: {},
                  })}
                >
                  {paginatedChunks[currentChunkIndex] || ""}
                </Text>
              </View>
            </View>
          </View>
        </GestureDetector>

        {/* ----- NO-SWIPE ZONE (tracker + page count) ----- */}
        <View style={{ paddingTop: 4 }}>
          <WordTracker
            width={containerWidth}
            activeIndex={activeWordIndex ?? 0}
            totalWords={chunkWordCount}
            marks={trackerMarks}
            triggerSet={triggerPositions}
            onSeekStart={onSeekStart}
            onSeekEnd={onSeekEnd}
          />
          <Text style={styles.progressText}>
            {currentPageInBook} of {totalPagesInBook} pages
          </Text>
        </View>

        {(optionsOpen || hasShownPanel) && (
          <Animated.View
            onLayout={(e) => {
              const h = e.nativeEvent.layout.height;
              setOptionsHeight(h);
              if (!hasMeasuredRef.current) {
                const closedY = -(h + insets.top + CLOSED_EXTRA);
                translateY.value = closedY;
                openProg.value = 0;
                hasMeasuredRef.current = true;
              }
            }}
            style={[
              styles.optionsPanel,
              {
                top: insets.top,
                maxHeight: SCREEN_H - insets.top - 24,
                overflow: "hidden",
              },
              optionsAnim,
            ]}
          >
            <ScrollView
              style={{ flex: 1 }}
              contentContainerStyle={{
                padding: 16,
                paddingBottom: 16 + insets.bottom,
              }}
              keyboardShouldPersistTaps="handled"
              showsVerticalScrollIndicator={false}
              nestedScrollEnabled
            >
              <ReadingControls
                wpm={wpm}
                ambienceVolPct={ambienceVolPct}
                triggerVolPct={triggerVolPct}
                fontSize={fontSize}
                onAnySliderStart={() => {}}
                onAnySliderEnd={() => {}}
                onWpmChange={(v) => {
                  setWpm(v);
                  save(STORAGE_KEYS.wpm, v);
                }}
                onAmbienceChange={(v) => {
                  setAmbienceVolPct(v);
                  SoundManager.setCarpetVolume(v / 100);
                  save(STORAGE_KEYS.ambVol, v);
                }}
                onTriggerChange={(v) => {
                  setTriggerVolPct(v);
                  SoundManager.setTriggerVolume(v / 100);
                  save(STORAGE_KEYS.trigVol, v);
                }}
                onFontSizeChange={(v) => {
                  const n = clampFont(v);
                  setFontSize(n);
                  save(STORAGE_KEYS.fontSize, n);
                }}
                onBackToLibrary={() => {
                  setOptionsOpen(false);
                  SoundManager.stopTriggers(200);
                  SoundManager.stopCarpet(300);
                  router.replace("/library");
                }}
                onClose={closeOptions}
                colors={{
                  text: COLORS.text,
                  subtext: COLORS.subtext,
                  accent: COLORS.accent,
                }}
              />
            </ScrollView>
          </Animated.View>
        )}
      </View>
    </SafeAreaView>
  );
}

/* -------- paragraph-aware invisible measurer (NEW) -------- */
function ParagraphMeasurer({
  paragraphs,
  fontSize,
  lineHeight,
  width,
  onMeasured,
}: {
  paragraphs: string[];
  fontSize: number;
  lineHeight: number;
  width: number;
  onMeasured: (lines: LineBox[]) => void;
}) {
  const collected = React.useRef<LineBox[]>([]);
  const remaining = React.useRef<number>(paragraphs.length);

  React.useEffect(() => {
    collected.current = [];
    remaining.current = paragraphs.length;
  }, [paragraphs, fontSize, lineHeight, width]);

  const flushIfDone = React.useCallback(() => {
    remaining.current -= 1;
    if (remaining.current === 0) {
      onMeasured(collected.current);
    }
  }, [onMeasured]);

  return (
    <View pointerEvents="none" collapsable={false} style={{ width }}>
      {paragraphs.map((para, idx) => (
        <View key={`para-${idx}`}>
          <Text
            style={{ fontSize, lineHeight, color: "transparent" }}
            allowFontScaling={false}
            onTextLayout={(e) => {
              const lines: LineBox[] = (e.nativeEvent.lines ?? []).map(
                (ln: any) => ({
                  text: String(ln.text || ""),
                  height: Number(ln.height) || lineHeight,
                })
              );
              collected.current.push(...lines);

              // ONE explicit spacer line between paragraphs
              if (idx < paragraphs.length - 1) {
                collected.current.push({
                  text: "", // renders as a blank line
                  height: lineHeight,
                  isSpacer: true,
                });
              }
              flushIfDone();
            }}
            {...Platform.select({
              android: {
                textBreakStrategy: "highQuality" as const,
                android_hyphenationFrequency: "none" as const,
              },
              default: {},
            })}
          >
            {para}
          </Text>
        </View>
      ))}
    </View>
  );
}

/* ========================= Helpers & Styles ========================= */
function clampFont(n: number) {
  if (!Number.isFinite(n)) return 16;
  return Math.max(FONT_MIN, Math.min(FONT_MAX, Math.round(n)));
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, paddingTop: 0, position: "relative" },
  bodyWrapper: { flex: 1 },
  pageText: {
    color: "#1F190F",
    includeFontPadding: false,
    // textAlign: "justify",
  },
  leftTouchable: {
    position: "absolute",
    top: "20%",
    left: 0,
    bottom: "10%",
    width: "40%",
    zIndex: 10,
    borderWidth: 1,
  },
  rightTouchable: {
    position: "absolute",
    top: "20%",
    right: 0,
    bottom: "10%",
    width: "40%",
    zIndex: 10,
  },
  progressContainer: { marginBottom: 0, zIndex: 1 },
  progressBar: { height: 2, backgroundColor: "transparent" },
  progressText: { color: "#1F190F", fontSize: 12, textAlign: "center" },
  pageCard: { flex: 1, backgroundColor: "transparent", marginBottom: 16 },
  chapterTitle: {
    marginTop: 16,
    fontWeight: "bold",
    color: "#1F190F",
    marginBottom: 8,
  },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
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
});
