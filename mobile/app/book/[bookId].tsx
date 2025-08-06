import React from "react";
import { useLocalSearchParams, useFocusEffect } from "expo-router";
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity, AppState } from "react-native";
import { ProgressBar } from "react-native-paper";
import { Dimensions } from "react-native";
import SoundManager from "../utils/soundManager";

const { height, width } = Dimensions.get("window");

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

import { useBook } from "../../hooks/useBooks";

const SOUND_MAP: Record<string, any> = {
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
  const { bookId } = useLocalSearchParams();
  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(0);
  const [currentPageIndex, setCurrentPageIndex] = React.useState(0);
  const [currentChunkIndex, setCurrentChunkIndex] = React.useState(0);
  const [paginatedChunks, setPaginatedChunks] = React.useState<string[]>([]);
  const [triggerWords, setTriggerWords] = React.useState<TriggerWord[]>([]);
  const [readingStartTime, setReadingStartTime] = React.useState<number>(0);
  const [isReading, setIsReading] = React.useState(false);
  const [activeTriggerWords, setActiveTriggerWords] = React.useState<Set<string>>(new Set());
  const [playedWords, setPlayedWords] = React.useState<Set<string>>(new Set());

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

  const paginateText = (text: string, fontSize = 16, lineHeight = 24) => {
    const words = text.split(/\s+/);
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

  const startReadingTimer = () => {
    setReadingStartTime(Date.now());
    setIsReading(true);
    setPlayedWords(new Set());
  };

  const stopReadingTimer = () => {
    setIsReading(false);
    setPlayedWords(new Set());
  };

  const calculateWordTiming = (text: string, wpm: number = 180) => {
    const words = text.split(/\s+/).filter((w) => w.length > 0);
    const msPerWord = 60_000 / wpm;
    return { words, msPerWord };
  };

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

  React.useEffect(() => {
    if (!isReading || triggerWords.length === 0) return;

    const checkTriggers = () => {
      const currentTime = Date.now() - readingStartTime;

      triggerWords.forEach((trigger) => {
        if (trigger.timing <= currentTime && trigger.timing > currentTime - 500) {
          if (!playedWords.has(trigger.id)) {
            setActiveTriggerWords(prev => new Set([...prev, trigger.id]));

            SoundManager.playTrigger(TRIGGER_WORDS[trigger.word]).then(() => {
              setActiveTriggerWords(prev => {
                const newSet = new Set(prev);
                newSet.delete(trigger.id);
                return newSet;
              });
            });

            setPlayedWords(prev => new Set([...prev, trigger.id]));
          }
        }
      });
    };

    const interval = setInterval(checkTriggers, 200);
    return () => clearInterval(interval);
  }, [isReading, triggerWords, readingStartTime, playedWords]);

  const renderTextWithHighlights = (text: string) => {
    const words = text.split(/(\s+)/);
    
    return (
      <Text style={styles.pageText}>
        {words.map((word, index) => {
          const clean = word.toLowerCase().replace(/[^\w]/g, "");
          const id = `${index}`; // isto kao gore
          const isActive = activeTriggerWords.has(id);

          return (
            <Text key={index} style={isActive ? styles.highlightedWord : undefined}>
              {word}
            </Text>
          );
        })}
      </Text>
    );
  };

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

  const goToNextPage = () => {
    if (currentChunkIndex < paginatedChunks.length - 1) {
      setCurrentChunkIndex(currentChunkIndex + 1);
      return;
    }
    if (currentPageIndex < totalPages - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
    } else if (currentChapterIndex < totalChapters - 1) {
      setCurrentChapterIndex(currentChapterIndex + 1);
      setCurrentPageIndex(0);
    }
  };

  const goToPreviousPage = () => {
    if (currentChunkIndex > 0) {
      setCurrentChunkIndex(currentChunkIndex - 1);
      return;
    }
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
    } else if (currentChapterIndex > 0) {
      const prevChapter = book?.chapters?.[currentChapterIndex - 1];
      const lastPageIndex = (prevChapter?.pages?.length || 1) - 1;
      setCurrentChapterIndex(currentChapterIndex - 1);
      setCurrentPageIndex(lastPageIndex);
    }
  };

  const loadSoundscapeForPage = async (chapterIndex?: number, pageIndex?: number) => {
    try {
      const targetChapterIndex = chapterIndex ?? currentChapterIndex;
      const targetPageIndex = pageIndex ?? currentPageIndex;

      stopReadingTimer();

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
      if (currentPage?.content) {
        const foundTriggers = findTriggerWords(currentPage.content);
        console.log("foundTriggers11111: ", foundTriggers);
        setTriggerWords(foundTriggers);
        if (foundTriggers.length > 0) {
          setTimeout(() => startReadingTimer(), 1000);
        }
      }
    } catch (error) {
      await SoundManager.stopAll();
    }
  };

  React.useEffect(() => {
    if (book && currentPage) {
      loadSoundscapeForPage(currentChapterIndex, currentPageIndex);
      const chunks = paginateText(currentPage.content);
      setPaginatedChunks(chunks);
      setCurrentChunkIndex(0);
    }
  }, [book, currentChapterIndex, currentPageIndex]);

  useFocusEffect(
    React.useCallback(() => {
      return () => {
        SoundManager.stopAll();
      };
    }, [])
  );

  React.useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => {
      if (s === "background" || s === "inactive") {
        SoundManager.stopAll();
      }
    });
    return () => sub.remove();
  }, []);

  React.useEffect(() => {
    return () => {
      SoundManager.stopAll();
    };
  }, []);

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
  } as any,
  pageInfo: { alignItems: "center", marginVertical: 12 },
  pageInfoText: { color: "#ccc", fontSize: 14, fontWeight: "500" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  highlightedWord: {
    backgroundColor: "#ff6b6b",
    padding: 2,
    borderRadius: 4,
  },
});
