import React from "react";
import { useLocalSearchParams } from "expo-router";
import { View, Text, StyleSheet, ActivityIndicator, ScrollView, TouchableOpacity, Alert } from "react-native";
import { Card, Button } from "react-native-paper";
import { Audio } from "expo-av";
import { Ionicons } from "@expo/vector-icons";

// -------------- ZVUČNA MAPA (lokalni asseti) --------------
import windyMountains from '../sounds/windy_mountains.mp3';
import defaultAmbience from '../sounds/default_ambience.mp3';
import tenseDrones from '../sounds/tense_drones.mp3';

const SOUND_MAP = {
  "windy_mountains.mp3": windyMountains,
  "default_ambience.mp3": defaultAmbience,
  "tense_drones.mp3": tenseDrones,
};

export default function BookDetailScreen() {
  const { bookId } = useLocalSearchParams();
  const [book, setBook] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [audioLoading, setAudioLoading] = React.useState(false);
  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(0);
  const [currentPageIndex, setCurrentPageIndex] = React.useState(0);
  const soundRef = React.useRef(null);

  // Get current page and chapter
  const currentChapter = book?.chapters?.[currentChapterIndex];
  const currentPage = currentChapter?.pages?.[currentPageIndex];
  const totalChapters = book?.chapters?.length || 0;
  const totalPages = currentChapter?.pages?.length || 0;

  // Navigation functions
  const goToNextPage = () => {
    if (currentPageIndex < totalPages - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
      loadSoundscapeForPage(currentChapterIndex, currentPageIndex + 1);
    } else if (currentChapterIndex < totalChapters - 1) {
      // Move to first page of next chapter
      setCurrentChapterIndex(currentChapterIndex + 1);
      setCurrentPageIndex(0);
      loadSoundscapeForPage(currentChapterIndex + 1, 0);
    }
  };

  const goToPreviousPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
      loadSoundscapeForPage(currentChapterIndex, currentPageIndex - 1);
    } else if (currentChapterIndex > 0) {
      // Move to last page of previous chapter
      const prevChapter = book?.chapters?.[currentChapterIndex - 1];
      const lastPageIndex = (prevChapter?.pages?.length || 1) - 1;
      setCurrentChapterIndex(currentChapterIndex - 1);
      setCurrentPageIndex(lastPageIndex);
      loadSoundscapeForPage(currentChapterIndex - 1, lastPageIndex);
    }
  };

  const loadSoundscapeForPage = async (chapterIndex: number, pageIndex: number) => {
    const chapter = book?.chapters?.[chapterIndex];
    const page = chapter?.pages?.[pageIndex];
    
    if (!chapter || !page) return;

    setAudioLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/soundscape/book/${bookId}/chapter${chapter.chapter_number}/page/${page.page_number}`
      );
      const soundscape = await response.json();
      
      // Stop current sound
      if (soundRef.current) {
        await soundRef.current.stopAsync();
        await soundRef.current.unloadAsync();
      }

      // Play new soundscape
      if (soundscape.carpet_tracks?.length > 0) {
        const track = soundscape.carpet_tracks[0];
        if (SOUND_MAP[track]) {
          const { sound } = await Audio.Sound.createAsync(SOUND_MAP[track]);
          soundRef.current = sound;
          await sound.playAsync();
        }
      }
    } catch (error) {
      console.warn("Error loading soundscape:", error);
    } finally {
      setAudioLoading(false);
    }
  };

  React.useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/books/${bookId}`)
      .then((response) => response.json())
      .then((data) => {
        setBook(data);
        setLoading(false);

        // Load soundscape for first page
        if (data.chapters?.[0]?.pages?.[0]) {
          loadSoundscapeForPage(0, 0);
        }
      })
      .catch(() => setLoading(false));

    // Cleanup: stop sound on unmount
    return () => {
      if (soundRef.current) {
        soundRef.current.unloadAsync();
      }
    };
  }, [bookId]);

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
        <Text>Greška pri učitavanju knjige.</Text>
      </View>
    );
  }

  if (!currentPage) {
    return (
      <View style={styles.center}>
        <Text>Ova knjiga nema strana.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header with book info */}
      <Card style={styles.headerCard}>
        <Card.Title title={book.title} subtitle={book.author} />
        <Card.Content>
          <Text style={styles.summary}>{book.summary}</Text>
        </Card.Content>
      </Card>

      {/* Page content */}
      <Card style={styles.pageCard}>
        <Card.Content>
          <Text style={styles.chapterTitle}>
            {currentChapter?.title
              ? `Poglavlje: ${currentChapter.title}`
              : `Poglavlje ${currentChapter?.chapter_number}`}
          </Text>
          <Text style={styles.pageNumber}>
            Strana {currentPage.page_number} od {totalPages}
          </Text>
          <Text style={styles.pageText}>{currentPage.content}</Text>
          {audioLoading && (
            <ActivityIndicator style={{ marginTop: 20 }} size="small" />
          )}
        </Card.Content>
      </Card>

      {/* Navigation controls */}
      <View style={styles.navigationContainer}>
        <TouchableOpacity
          style={[
            styles.navButton,
            (currentChapterIndex === 0 && currentPageIndex === 0) && styles.disabledButton
          ]}
          onPress={goToPreviousPage}
          disabled={currentChapterIndex === 0 && currentPageIndex === 0}
        >
          <Ionicons name="chevron-back" size={24} color="#fff" />
          <Text style={styles.navButtonText}>Prethodna</Text>
        </TouchableOpacity>

        <View style={styles.pageInfo}>
          <Text style={styles.pageInfoText}>
            {currentChapterIndex + 1}/{totalChapters} • {currentPageIndex + 1}/{totalPages}
          </Text>
        </View>

        <TouchableOpacity
          style={[
            styles.navButton,
            (currentChapterIndex === totalChapters - 1 && currentPageIndex === totalPages - 1) && styles.disabledButton
          ]}
          onPress={goToNextPage}
          disabled={currentChapterIndex === totalChapters - 1 && currentPageIndex === totalPages - 1}
        >
          <Text style={styles.navButtonText}>Sljedeća</Text>
          <Ionicons name="chevron-forward" size={24} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: "#1a1a1a",
  },
  headerCard: {
    marginBottom: 16,
    backgroundColor: "#2a2a2a",
  },
  pageCard: {
    flex: 1,
    backgroundColor: "#2a2a2a",
    marginBottom: 16,
  },
  summary: {
    marginBottom: 16,
    color: "#fff",
  },
  chapterTitle: {
    marginTop: 16,
    fontWeight: "bold",
    fontSize: 18,
    color: "#fff",
    marginBottom: 8,
  },
  pageNumber: {
    fontSize: 14,
    color: "#ccc",
    marginBottom: 16,
    textAlign: "center",
  },
  pageText: {
    fontSize: 16,
    color: "#fff",
    lineHeight: 24,
  },
  navigationContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 16,
    backgroundColor: "#2a2a2a",
    borderRadius: 8,
  },
  navButton: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: "#4a4a4a",
    borderRadius: 8,
    minWidth: 100,
    justifyContent: "center",
  },
  disabledButton: {
    backgroundColor: "#3a3a3a",
    opacity: 0.5,
  },
  navButtonText: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "500",
    marginHorizontal: 4,
  },
  pageInfo: {
    alignItems: "center",
  },
  pageInfoText: {
    color: "#ccc",
    fontSize: 14,
    fontWeight: "500",
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});
