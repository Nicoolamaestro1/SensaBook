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

const API_BASE = `${API_HOST}/api/soundscape`;

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
  console.log(`Fetching soundscape: ${API_BASE}/book/${bookId}`);
  const res = await fetch(
    `${API_BASE}/book/${bookId}/chapter/${chapterNumber}/page/${pageNumber}`
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

  React.useEffect(() => {
    if (book) {
      console.log("📚 Current book data:", JSON.stringify(book, null, 2));
    }
  }, [book]);

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
          setActiveTriggerWords((prevSet) => {
            const s = new Set(prevSet);
            s.add(trig.id);
            return s;
          });
          SoundManager.playTrigger(WORD_TRIGGERS[trig.word]).finally(() => {
            setActiveTriggerWords((prevSet) => {
              const s = new Set(prevSet);
              s.delete(trig.id);
              return s;
            });
          });
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

  const loadSoundscapeForPage = async (
    chapterIndex?: number,
    pageIndex?: number
  ) => {
    const ci = chapterIndex ?? currentChapterIndex;
    const pi = pageIndex ?? currentPageIndex;

    // try server first
    try {
      if (!book) throw new Error("no book");
      const data = await fetchSoundscape(bookId as string, ci, pi);

      // pick first recommended carpet
      const first = data.carpet_tracks?.[0];
      if (first && SOUND_MAP[first]) {
        await SoundManager.playCarpet(SOUND_MAP[first], first);

        // OPTIONAL: use server-provided triggers instead of local detection
        // setTriggerWords(
        //   data.triggered_sounds.map((t, i) => ({
        //     id: String(i),
        //     word: t.word.toLowerCase(),
        //     position: t.position,
        //     timing: 0, // you can recompute using your msPerWord
        //   }))
        // );

        return; // success via API, stop here
      }
    } catch (err) {
      // silent fallback below
      // console.log("Soundscape API fallback:", err);
    }

    // --- fallback to your local mapping if API fails or returns unknown file ---
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
    if (!asset) return;

    await SoundManager.playCarpet(asset, ambienceKey);
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
