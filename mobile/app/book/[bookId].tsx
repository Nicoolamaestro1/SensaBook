import React from "react";
import { useLocalSearchParams, useRouter, useFocusEffect } from "expo-router";
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity, AppState } from "react-native";
import { ProgressBar } from "react-native-paper";
import { Dimensions } from "react-native";
import SoundManager from "../utils/soundManager";
import { useBook } from "../../hooks/useBooks";
import { ReadingSpeed } from "../options";

import windyMountains from "../sounds/windy_mountains.mp3";
import defaultAmbience from "../sounds/default_ambience.mp3";
import tenseDrones from "../sounds/tense_drones.mp3";
import footstepsApproaching from "../sounds/footsteps-approaching-316715.mp3";
import atmosphereSound from "../sounds/atmosphere-sound-effect-239969.mp3";
import thunderCity from "../sounds/thunder-city-377703.mp3";
import stormyNight from "../sounds/stormy_night.mp3";
import storm from "../sounds/storm.mp3";
import cabinRain from "../sounds/cabin_rain.mp3";
import cabin from "../sounds/cabin.mp3";
import windHowl from "../sounds/wind.mp3";

const { height, width } = Dimensions.get("window");

const SOUND_MAP: Record<string, any> = {
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

interface TriggerWord {
  id: string;
  word: string;
  position: number;
  timing: number;
}

export default function BookDetailScreen() {
  // ---- URL-based navigation state ----
  const params = useLocalSearchParams();
  const router = useRouter();

  // Initial state from URL (on first render), always numbers
  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(Number(params.chapter ?? 0));
  const [currentPageIndex, setCurrentPageIndex] = React.useState(Number(params.page ?? 0));
  const [currentChunkIndex, setCurrentChunkIndex] = React.useState(Number(params.chunk ?? 0));
  const [paginatedChunks, setPaginatedChunks] = React.useState<string[]>([]);
  const [triggerWords, setTriggerWords] = React.useState<TriggerWord[]>([]);
  const [activeTriggerWords, setActiveTriggerWords] = React.useState<Set<string>>(new Set());
  const [activeWordIndex, setActiveWordIndex] = React.useState<number | null>(null);

  const wordIntervalRef = React.useRef<NodeJS.Timeout | null>(null);

  // Your data
  const { bookId, readingSpeed: readingSpeedParam } = params;
  const { book, loading } = useBook(bookId as string) as {
    book: any;
    loading: boolean;
  };

  const TRIGGER_WORDS: Record<string, any> = {
    thunder: thunderCity,
    footsteps: footstepsApproaching,
    wind: windHowl,
    storm: storm,
  };

  // --- Keep position in URL (write to params on every change) ---
  React.useEffect(() => {
    router.setParams({
      chapter: String(currentChapterIndex),
      page: String(currentPageIndex),
      chunk: String(currentChunkIndex)
    });
    // eslint-disable-next-line
  }, [currentChapterIndex, currentPageIndex, currentChunkIndex]);

  // --- If route param changes externally, update state (for back/forward buttons) ---
  React.useEffect(() => {
    if (params.chapter !== undefined) setCurrentChapterIndex(Number(params.chapter));
    if (params.page !== undefined) setCurrentPageIndex(Number(params.page));
    if (params.chunk !== undefined) setCurrentChunkIndex(Number(params.chunk));
    // eslint-disable-next-line
  }, [params.chapter, params.page, params.chunk]);

  // Paginates the text for the book screen
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

  const readingSpeedMap: Record<ReadingSpeed, number> =  {
    "slow": 100,
    "avarage": 200,
    "fast": 300,
  }

  // Calculates ms per word (reading speed)
  const calculateWordTiming = (text: string) => {
    if (!text) return { words: [], msPerWord: 333 };
    const words = text.split(/\s+/).filter(Boolean);
    const readingSpeed = readingSpeedMap[readingSpeedParam as ReadingSpeed];
    const msPerWord = readingSpeed ? 60_000 / readingSpeed : 200;
    return { words, msPerWord };
  };
  
  // Finds trigger words in text
  const findTriggerWords = (text: string) => {
    const { words, msPerWord } = calculateWordTiming(text);
    const found: TriggerWord[] = [];
    words.forEach((word, index) => {
      const clean = word.toLowerCase().replace(/[^\w]/g, "");
      if (TRIGGER_WORDS[clean]) {
        found.push({
          id: `${index}`,
          word: clean,
          position: index,
          timing: index * msPerWord,
        });
      }
    });
    return found;
  };

  // Stops the reading timer and all highlight/trigger states
  const stopReadingTimer = React.useCallback(() => {
    setActiveTriggerWords(new Set());
    setActiveWordIndex(null);
    if (wordIntervalRef.current) {
      clearInterval(wordIntervalRef.current);
      wordIntervalRef.current = null;
    }
  }, []);

  // Starts the reading timer, highlights words and plays triggers
  const startReadingTimer = React.useCallback(() => {
    stopReadingTimer();
    setActiveTriggerWords(new Set());
    setActiveWordIndex(0);

    const chunk = paginatedChunks[currentChunkIndex] || "";
    const { words, msPerWord } = calculateWordTiming(chunk);

    let idx = 0;
    wordIntervalRef.current = setInterval(() => {
      setActiveWordIndex((prev) => {
        const currentIdx = prev === null ? 0 : prev + 1;

        // Check if this is a trigger word
        const trigger = triggerWords.find(t => t.position === currentIdx);
        if (trigger && !activeTriggerWords.has(trigger.id)) {
          setActiveTriggerWords(prevSet => {
            const newSet = new Set(prevSet);
            newSet.add(trigger.id);
            return newSet;
          });
          SoundManager.playTrigger(TRIGGER_WORDS[trigger.word]).then(() => {
            setActiveTriggerWords(prevSet => {
              const newSet = new Set(prevSet);
              newSet.delete(trigger.id);
              return newSet;
            });
          });
        }

        if (currentIdx >= words.length) {
          stopReadingTimer();
          return null;
        }
        return currentIdx;
      });
      idx++;
    }, msPerWord);
  // eslint-disable-next-line
  }, [paginatedChunks, currentChunkIndex, triggerWords, activeTriggerWords, stopReadingTimer]);

  // --- Main page navigation ---
  const currentChapter = book?.chapters?.[currentChapterIndex];
  const currentPage = currentChapter?.pages?.[currentPageIndex];
  const totalChapters = book?.chapters?.length || 0;
  const totalPages = currentChapter?.pages?.length || 0;

  const totalPagesInBook =
    book?.chapters?.reduce(
      (total: number, chapter: any) => total + chapter.pages.length,
      0
    ) || 0;
  const currentPageInBook =
    book?.chapters
      ?.slice(0, currentChapterIndex)
      .reduce((total: number, chapter: any) => total + chapter.pages.length, 0) +
      currentPageIndex +
      1 || 0;
  const readingProgress =
    totalPagesInBook > 0 ? currentPageInBook / totalPagesInBook : 0;

  // Go to next page or chunk
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

  // Go to previous page or chunk
  const goToPreviousPage = () => {
    stopReadingTimer();
    if (currentChapterIndex === 0 && currentPageIndex === 0 && currentChunkIndex === 0) {
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

  // Loads ambient soundscape for the page and starts carpet audio if needed
  const loadSoundscapeForPage = async (chapterIndex?: number, pageIndex?: number) => {
    try {
      const targetChapterIndex = chapterIndex ?? currentChapterIndex;
      const targetPageIndex = pageIndex ?? currentPageIndex;
      await SoundManager.stopAll();

      const response = await fetch(
        `http://localhost:8000/soundscape/book/${bookId}/chapter${targetChapterIndex + 1}/page/${targetPageIndex + 1}`
      );

      if (!response.ok) {
        await SoundManager.stopAll();
        return;
      }

      const data = await response.json();
      if (!data) {
        await SoundManager.stopAll();
        return;
      }
      if (data.carpet_tracks && data.carpet_tracks.length > 0) {
        const soundFile = data.carpet_tracks[0];
        const soundAsset = SOUND_MAP[soundFile];
        if (soundAsset) {
          await SoundManager.playCarpet(soundAsset);
        }
      } else {
        await SoundManager.stopAll();
      }
    } catch (error) {
      await SoundManager.stopAll();
    }
  };

  // First set paginatedChunks and reset chunk index to 0 when page changes
  React.useEffect(() => {
    if (book && currentPage) {
      const chunks = paginateText(currentPage.content);
      setPaginatedChunks(chunks);
      setCurrentChunkIndex(0);
    }
    // eslint-disable-next-line
  }, [book, currentChapterIndex, currentPageIndex]);

  // When paginatedChunks or chunkIndex changes, find trigger words and load soundscape, and start reading when all is ready
  React.useEffect(() => {
    if (
      book && 
      book.chapters?.[currentChapterIndex]?.pages?.[currentPageIndex] &&
      paginatedChunks.length > 0
    ) {
      const chunk = paginatedChunks[currentChunkIndex];
      setTriggerWords(findTriggerWords(chunk));
      loadSoundscapeForPage(currentChapterIndex, currentPageIndex);
      startReadingTimer();
    }
    // eslint-disable-next-line
  }, [book, currentChapterIndex, currentPageIndex, currentChunkIndex, paginatedChunks.length]);

  // When triggerWords change, start reading timer
  React.useEffect(() => {
    if (paginatedChunks.length > 0 && triggerWords) {
      startReadingTimer();
    }
  }, [triggerWords, paginatedChunks, currentChunkIndex, currentChapterIndex, currentPageIndex]);

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

  React.useEffect(() => {
    return () => {
      SoundManager.stopAll();
      stopReadingTimer();
    };
  }, [stopReadingTimer]);

  // --- Render words with highlights ---
  const renderTextWithHighlights = (text: string) => {
    const words = text.split(/\s+/).filter(Boolean);
    return (
     <Text style={styles.pageText}>
        {words.map((word, index) => {
          const clean = word.toLowerCase().replace(/[^\w]/g, "");
          const trigger = triggerWords.find(t => t.position === index);
          const isActiveTrigger = activeTriggerWords.has(`${index}`);
          const isActiveReading = activeWordIndex === index;

          let style = undefined;
          if (isActiveTrigger) style = styles.triggerHighlight;
          else if (isActiveReading) style = styles.wordBorderHighlight;

          return (
            <Text key={index} style={style}>
              {word}{index !== words.length - 1 ? " " : ""}
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

  return (
    <>
      <View style={styles.progressContainer}>
        <ProgressBar
          progress={readingProgress}
          color="#5b4636"
          style={styles.progressBar}
        />
        <Text style={styles.progressText}>
          {currentPageInBook} of {totalPagesInBook} pages
        </Text>
      </View>
      <View style={styles.container}>
        <TouchableOpacity style={styles.leftTouchable} onPress={goToPreviousPage} activeOpacity={1} />
        <TouchableOpacity style={styles.rightTouchable} onPress={goToNextPage} activeOpacity={1} />
        <View style={styles.pageCard}>
          <Text style={styles.chapterTitle}>
            {currentChapter?.title
              ? `Chapter: ${currentChapter.title}`
              : `Chapter ${currentChapter?.chapter_number}`}
          </Text>
          <Text style={styles.pageText}>
            {renderTextWithHighlights(paginatedChunks[currentChunkIndex] || "")}
          </Text>
        </View>
        <View style={styles.pageInfo}>
          <Text style={styles.pageInfoText}>
            {currentChapterIndex + 1}/{totalChapters} • {currentPageIndex + 1}/{totalPages}
          </Text>
        </View>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, paddingTop: 0, position: "relative" },
  leftTouchable: {
    position: "absolute",
    top: 0,
    left: 0,
    bottom: 0,
    width: "40%",
    zIndex: 10,
  },
  rightTouchable: {
    position: "absolute",
    top: 0,
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
  pageInfo: { alignItems: "center", marginVertical: 12 },
  pageInfoText: { color: "#ccc", fontSize: 14, fontWeight: "500" },
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
});
