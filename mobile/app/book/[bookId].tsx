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
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ProgressBar } from "react-native-paper";
import Animated, {
  useSharedValue,
  withTiming,
  useAnimatedStyle,
} from "react-native-reanimated";
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
  paginateText,
  computeReadingProgress,
} from "../utils/reading";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import AsyncStorage from "@react-native-async-storage/async-storage";
import type { Book, Chapter, Page } from "../../types/book";
import type { SoundscapeResponse } from "../../types/soundscape";
import ReadingControls from "../components/ReadingControls";
import { buildSoundscapeUrl, logSoundscapeRequest } from "../config/api";
import { GestureDetector, Gesture } from "react-native-gesture-handler";
import { runOnJS } from 'react-native-reanimated';
  
/* =====================================================
   THEME & CONSTANTS
   ===================================================== */
const COLORS = Object.freeze({
  card: "#17171c",
  text: "#EAEAF0",
  subtext: "#A6A8B1",
  border: "rgba(255,255,255,0.06)",
  accent: "#FF7A18",
});

const STORAGE_KEYS = Object.freeze({
  wpm: "settings.wpm",
  ambVol: "settings.ambienceVolPct",
  trigVol: "settings.triggerVolPct",
  fontSize: "settings.fontSizePt", // ✅ add font-size key
});

const FONT_MIN = 12;
const FONT_MAX = 28;

const { height: SCREEN_H } = Dimensions.get("window");
const PANEL_MARGIN = 12;
const { height, width } = Dimensions.get("window");

/* =====================================================
   TYPES
   ===================================================== */
type TimeoutId = ReturnType<typeof setTimeout>;

/* =====================================================
   COMPONENT
   ===================================================== */
export default function BookDetailScreen() {
  /* ---------- Navigation & Safe Area ---------- */
  const params = useLocalSearchParams();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  /* ---------- Animation State ---------- */
  const CLOSED_EXTRA = 40;
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

  // Volumes (percent) + WPM + FONT SIZE ✅
  const [ambienceVolPct, setAmbienceVolPct] = React.useState(60);
  const [triggerVolPct, setTriggerVolPct] = React.useState(80);
  const [fontSize, setFontSize] = React.useState<number>(16); // ✅ add font size state
  const { wpm, setWpm } = useWpm();

  // Derived line height for pagination & rendering
  const lineHeight = Math.max(Math.round(fontSize * 1.5), fontSize + 6); // simple readable rule

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
    book: Book | null;
    loading: boolean;
  };

  const currentChapter: Chapter | undefined =
    book?.chapters?.[currentChapterIndex];
  const currentPage: Page | undefined =
    currentChapter?.pages?.[currentPageIndex];
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
  React.useEffect(() => {
    (async () => {
      try {
        const [w, a, t, f] = await Promise.all([
          AsyncStorage.getItem(STORAGE_KEYS.wpm),
          AsyncStorage.getItem(STORAGE_KEYS.ambVol),
          AsyncStorage.getItem(STORAGE_KEYS.trigVol),
          AsyncStorage.getItem(STORAGE_KEYS.fontSize), // ✅ load font size
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
      } catch {
        // swallow
      }
    })();
  }, [setWpm]);

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
              SoundManager.playTrigger(asset).finally(() => {
                setActiveTriggerWords((prev) => {
                  const s = new Set(prev);
                  s.delete(trig.id);
                  return s;
                });
              });
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
     NAVIGATION
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
     SOUNDSCAPE LOADING
     ===================================================== */
  const loadSoundscapeForPage = React.useCallback(
    async (chapterIndex?: number, pageIndex?: number) => {
      if (!book) return;

      const ci = chapterIndex ?? currentChapterIndex;
      const pi = pageIndex ?? currentPageIndex;

      const chapterNumber = book.chapters?.[ci]?.chapter_number ?? ci + 1;
      const pageNumber =
        book.chapters?.[ci]?.pages?.[pi]?.page_number ?? pi + 1;

      logSoundscapeRequest(Number(bookId), chapterNumber, pageNumber);

      try {
        const data: SoundscapeResponse = await fetchSoundscape(
          Number(bookId),
          chapterNumber,
          pageNumber
        );
        const chunkText = paginatedChunks[currentChunkIndex] || "";
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
          .filter(
            (tw: TriggerWord) =>
              tw.position >= 0 && tw.position < chunkTokens.length
          );

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
        return;
      } catch (err) {
        console.log("Soundscape API fallback:", err);
      }

      // fallback
      const page = book?.chapters?.[ci]?.pages?.[pi];
      let ambienceKey = page?.ambient as string | undefined;
      if (!ambienceKey) {
        const pageAmbienceMap: Record<string, string> = {
          "0-0": "ambience/windy_mountains.mp3",
          "0-1": "ambience/cabin_rain.mp3",
          "1-0": "ambience/stormy_night.mp3",
        };
        ambienceKey =
          pageAmbienceMap[`${ci}-${pi}`] || "ambience/default_ambience.mp3";
      }
      const asset = SOUND_MAP[ambienceKey];
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
  React.useEffect(() => {
    return () => {
      SoundManager.stopCarpet();
    };
  }, [bookId]);

  // ✅ paginate using current font metrics
  React.useEffect(() => {
    if (book && currentPage) {
      const chunks = paginateText(
        currentPage.content,
        { width, height },
        { fontSize, lineHeight } // ✅ use live font size
      );
      setPaginatedChunks(chunks);
      setCurrentChunkIndex(0);
    }
  }, [
    book,
    currentChapterIndex,
    currentPageIndex,
    currentPage,
    fontSize,
    lineHeight,
  ]);

  React.useEffect(() => {
    if (
      book &&
      book.chapters?.[currentChapterIndex]?.pages?.[currentPageIndex] &&
      paginatedChunks.length > 0
    ) {
      const chunk = paginatedChunks[currentChunkIndex];
      const { words, msPerWord } = calculateWordTiming(
        chunk,
        wpmRef.current || 200
      );
      const triggers = findTriggerWords(words, msPerWord);
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
      <Text style={[styles.pageText, { fontSize, lineHeight }]}>
        {words.map((word, index) => {
          const trigger = triggerWords.find((t) => t.position === index);
          const isActiveTrigger = trigger
            ? activeTriggerWords.has(trigger.id)
            : false;
          const isActiveReading = activeWordIndex === index;

          let style: any | undefined = undefined;
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

  const {
    totalPagesInBook,
    currentPageInBook,
    progress: readingProgress,
  } = computeReadingProgress(book, currentChapterIndex, currentPageIndex);

  const swipe = Gesture.Pan().onEnd((event) => {
    const { translationX, translationY } = event;

    if (Math.abs(translationX) > Math.abs(translationY)) {
      if (translationX > 0) {
        runOnJS(goToPreviousPage)();
      } else {
        runOnJS(goToNextPage)();
      }
    } else {
      if (translationY > 0) {
        runOnJS(openOptions)();
      } else {
        runOnJS(closeOptions)();
      }
    }
  });

  return (
    <GestureDetector gesture={swipe}>
      <SafeAreaView style={{ flex: 1 }}>
      <View style={styles.progressContainer}>
        <ProgressBar
          progress={readingProgress}
          color="#5b4636"
          style={styles.progressBar}
        />
      </View>

      <View style={styles.container}>
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
                // ✅ constrain height so ScrollView can actually scroll
                maxHeight: SCREEN_H - insets.top - PANEL_MARGIN * 2,
                overflow: "hidden", // clip big content behind rounded corners
              },
              optionsAnim,
            ]}
          >
            <ScrollView
              style={{ flex: 1 }} // ✅ fill the constrained panel
              contentContainerStyle={{
                padding: 16,
                paddingBottom: 16 + insets.bottom, // a little extra for safe-area
              }}
              showsVerticalScrollIndicator
              keyboardShouldPersistTaps="handled"
              nestedScrollEnabled
            >
              <ReadingControls
                wpm={wpm}
                ambienceVolPct={ambienceVolPct}
                triggerVolPct={triggerVolPct}
                fontSize={fontSize}
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
    </GestureDetector>
  );
}

/* =====================================================
   HELPERS & STYLES
   ===================================================== */
function clampFont(n: number) {
  if (!Number.isFinite(n)) return 16;
  return Math.max(FONT_MIN, Math.min(FONT_MAX, Math.round(n)));
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
    // fontSize & lineHeight are injected dynamically
    color: "#5b4636",
    textAlign: "justify" as const,
  },
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
