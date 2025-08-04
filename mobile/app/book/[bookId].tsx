import React from "react";
import { useLocalSearchParams } from "expo-router";
import { View, Text, StyleSheet, ActivityIndicator, ScrollView, TouchableOpacity, Alert } from "react-native";
import { Card, ProgressBar } from "react-native-paper";
import { Audio } from "expo-av";
import { Ionicons } from "@expo/vector-icons";

// -------------- SOUND MAP (local assets) --------------
import windyMountains from '../sounds/windy_mountains.mp3'; 
import defaultAmbience from '../sounds/default_ambience.mp3';
import tenseDrones from '../sounds/tense_drones.mp3';
import footstepsApproaching from '../sounds/footsteps-approaching-316715.mp3';
import atmosphereSound from '../sounds/atmosphere-sound-effect-239969.mp3';
import thunderCity from '../sounds/thunder-city-377703.mp3';
import stormyNight from '../sounds/stormy_night.mp3';
import storm from '../sounds/storm.mp3';

const SOUND_MAP = {
  "windy_mountains.mp3": windyMountains,
  "default_ambience.mp3": defaultAmbience,
  "tense_drones.mp3": tenseDrones,
  "footsteps-approaching-316715.mp3": footstepsApproaching,
  "atmosphere-sound-effect-239969.mp3": atmosphereSound,
  "thunder-city-377703.mp3": thunderCity,
  "stormy_night.mp3": stormyNight,
  "storm.mp3": storm,
};

export default function BookDetailScreen() {
  const { bookId } = useLocalSearchParams();
  const [book, setBook] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);
  const [currentChapterIndex, setCurrentChapterIndex] = React.useState(0);
  const [currentPageIndex, setCurrentPageIndex] = React.useState(0);
  const [sound, setSound] = React.useState<Audio.Sound | null>(null);
  const [triggerWords, setTriggerWords] = React.useState<Array<{word: string, position: number, timing: number}>>([]);
  const [readingStartTime, setReadingStartTime] = React.useState<number>(0);
  const [isReading, setIsReading] = React.useState(false);
  const [activeTriggerWords, setActiveTriggerWords] = React.useState<Set<string>>(new Set());
  const [playedWords, setPlayedWords] = React.useState<Set<string>>(new Set()); // Track played words to prevent duplicates

  // Trigger words and their corresponding sounds
  const TRIGGER_WORDS = {
    'thunder': thunderCity, // Using thunder city sound for thunder
    'footsteps': footstepsApproaching,
    'rain': atmosphereSound, // Using atmosphere sound for rain since rain-sound-188158.mp3 doesn't exist
    'wind': windyMountains,
    'storm': storm, // Using storm.mp3 for storm
  };

  // Calculate reading timing based on word count and estimated reading speed
  const calculateWordTiming = (text: string, estimatedReadingTimeMinutes: number = 0.5) => {
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const totalWords = words.length;
    const readingTimeMs = estimatedReadingTimeMinutes * 60 * 1000; // Convert to milliseconds
    const msPerWord = readingTimeMs / totalWords;
    
    return { words, msPerWord, totalWords };
  };

  // Find trigger words and calculate their timing
  const findTriggerWords = (text: string) => {
    const { words, msPerWord } = calculateWordTiming(text);
    const foundTriggers: Array<{word: string, position: number, timing: number}> = [];
    
    words.forEach((word, index) => {
      const lowerWord = word.toLowerCase().replace(/[^\w]/g, '');
      if (TRIGGER_WORDS[lowerWord as keyof typeof TRIGGER_WORDS]) {
        foundTriggers.push({
          word: lowerWord,
          position: index,
          timing: index * msPerWord
        });
      }
    });
    
    return foundTriggers;
  };

  // Start reading timer
  const startReadingTimer = () => {
    setReadingStartTime(Date.now());
    setIsReading(true);
    setPlayedWords(new Set()); // Reset played words when starting new reading session
  };

  // Stop reading timer
  const stopReadingTimer = () => {
    setIsReading(false);
    setPlayedWords(new Set()); // Clear played words when stopping
  };

  // Check for trigger words and play sounds
  React.useEffect(() => {
    if (!isReading || triggerWords.length === 0) return;

    const checkTriggers = () => {
      const currentTime = Date.now() - readingStartTime;
      
      triggerWords.forEach(trigger => {
        if (trigger.timing <= currentTime && trigger.timing > currentTime - 1000) { // Within 1 second window
          // Only play if this word hasn't been played yet
          if (!playedWords.has(trigger.word)) {
            playTriggerSound(trigger.word);
            setPlayedWords(prev => new Set([...prev, trigger.word])); // Mark as played
          }
        }
      });
    };

    const interval = setInterval(checkTriggers, 100); // Check every 100ms
    return () => clearInterval(interval);
  }, [isReading, triggerWords, readingStartTime, playedWords]);

  // Play trigger sound
  const playTriggerSound = async (word: string) => {
    try {
      const soundAsset = TRIGGER_WORDS[word as keyof typeof TRIGGER_WORDS];
      if (soundAsset) {
        // Add word to active set for visual highlighting
        setActiveTriggerWords(prev => new Set([...prev, word]));
        
        const { sound: newSound } = await Audio.Sound.createAsync(soundAsset, {
          shouldPlay: true,
          isLooping: false,
          volume: 0.8,
        });
        
        // Remove word from active set after sound finishes
        setTimeout(() => {
          setActiveTriggerWords(prev => {
            const newSet = new Set(prev);
            newSet.delete(word);
            return newSet;
          });
        }, 3000); // Match the cleanup timeout
        
        // Clean up after sound plays
        setTimeout(() => {
          newSound.unloadAsync();
        }, 3000); // Clean up after 3 seconds
      }
    } catch (error) {
      console.log("Error playing trigger sound:", error);
    }
  };

  // Render text with highlighted trigger words
  const renderTextWithHighlights = (text: string) => {
    const words = text.split(/(\s+)/);
    return (
      <Text style={styles.pageText}>
        {words.map((word, index) => {
          const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
          const isActive = activeTriggerWords.has(cleanWord);
          
          if (isActive) {
            return (
              <Text key={index} style={styles.highlightedWord}>
                {word}
              </Text>
            );
          }
          return word;
        })}
      </Text>
    );
  };

  // Get current page and chapter
  const currentChapter = book?.chapters?.[currentChapterIndex];
  const currentPage = currentChapter?.pages?.[currentPageIndex];
  const totalChapters = book?.chapters?.length || 0;
  const totalPages = currentChapter?.pages?.length || 0;

  // Calculate reading progress
  const totalPagesInBook = book?.chapters?.reduce((total: number, chapter: any) => total + chapter.pages.length, 0) || 0;
  const currentPageInBook = book?.chapters?.slice(0, currentChapterIndex).reduce((total: number, chapter: any) => total + chapter.pages.length, 0) + currentPageIndex + 1 || 0;
  const readingProgress = totalPagesInBook > 0 ? currentPageInBook / totalPagesInBook : 0;

  // Navigation functions
  const goToNextPage = () => {
    if (currentPageIndex < totalPages - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
      loadSoundscapeForPage();
    } else if (currentChapterIndex < totalChapters - 1) {
      // Move to first page of next chapter
      setCurrentChapterIndex(currentChapterIndex + 1);
      setCurrentPageIndex(0);
      loadSoundscapeForPage();
    }
  };

  const goToPreviousPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
      loadSoundscapeForPage();
    } else if (currentChapterIndex > 0) {
      // Move to last page of previous chapter
      const prevChapter = book?.chapters?.[currentChapterIndex - 1];
      const lastPageIndex = (prevChapter?.pages?.length || 1) - 1;
      setCurrentChapterIndex(currentChapterIndex - 1);
      setCurrentPageIndex(lastPageIndex);
      loadSoundscapeForPage();
    }
  };

  // Load soundscape for current page
  const loadSoundscapeForPage = async () => {
    try {
      if (sound) {
        await sound.unloadAsync();
      }

      // Stop any ongoing reading timer
      stopReadingTimer();

      const response = await fetch(`http://localhost:8000/soundscape/book/${bookId}/chapter${currentChapterIndex + 1}/page/${currentPageIndex + 1}`);
      const soundscapeData = await response.json();
      
      if (soundscapeData.carpet_tracks && soundscapeData.carpet_tracks.length > 0) {
        const soundFile = soundscapeData.carpet_tracks[0];
        const soundAsset = SOUND_MAP[soundFile as keyof typeof SOUND_MAP];
        
        if (soundAsset) {
          const { sound: newSound } = await Audio.Sound.createAsync(soundAsset, {
            shouldPlay: true,
            isLooping: true,
            volume: 0.5,
          });
          setSound(newSound);
        }
      }

      // Find trigger words in current page content
      if (currentPage?.content) {
        const foundTriggers = findTriggerWords(currentPage.content);
        setTriggerWords(foundTriggers);
        console.log(`Found ${foundTriggers.length} trigger words:`, foundTriggers);
        
        // Auto-start reading timer if trigger words are found
        if (foundTriggers.length > 0) {
          setTimeout(() => {
            startReadingTimer();
          }, 1000); // Start reading after 1 second delay
        }
      }
    } catch (error) {
      console.log("Error loading soundscape:", error);
    }
  };

  React.useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/books/${bookId}`)
      .then((response) => response.json())
      .then((data) => {
        setBook(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));

    // Cleanup: stop sound on unmount
    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, [bookId]);

  // Load soundscape when book data is available and page changes
  React.useEffect(() => {
    if (book && currentPage) {
      loadSoundscapeForPage();
    }
  }, [book, currentChapterIndex, currentPageIndex]);

  // Cleanup effect to stop sounds when component unmounts
  React.useEffect(() => {
    return () => {
      // Stop carpet sound when component unmounts
      if (sound) {
        sound.unloadAsync();
      }
      // Stop any ongoing reading timer
      stopReadingTimer();
    };
  }, [sound]); // Depend on sound to ensure cleanup runs when sound changes

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
    <View style={styles.container}>
      {/* Progress bar */}
      <View style={styles.progressContainer}>
        <ProgressBar 
          progress={readingProgress} 
          color="#4CAF50" 
          style={styles.progressBar}
        />
        <Text style={styles.progressText}>
          {currentPageInBook} of {totalPagesInBook} pages
        </Text>
      </View>

      {/* Header with book info */}
      <Card style={styles.headerCard}>
        <Card.Title title={book.title} subtitle={book.author} />
        <Card.Content>
          <Text style={styles.summary}>{book.summary}</Text>
        </Card.Content>
      </Card>

      {/* Page content */}
      <View style={styles.pageContainer}>
        <Card style={styles.pageCard}>
          <Card.Content>
            <Text style={styles.chapterTitle}>
              {currentChapter?.title
                ? `Chapter: ${currentChapter.title}`
                : `Chapter ${currentChapter?.chapter_number}`}
            </Text>
            <Text style={styles.pageNumber}>
              Page {currentPage.page_number} of {totalPages}
            </Text>
            <Text style={styles.pageText}>
              {renderTextWithHighlights(currentPage.content)}
            </Text>
          </Card.Content>
        </Card>
      </View>

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
          <Text style={styles.navButtonText}>Previous</Text>
        </TouchableOpacity>

        <View style={styles.pageInfo}>
          <Text style={styles.pageInfoText}>
            {currentChapterIndex + 1}/{totalChapters} • {currentPageIndex + 1}/{totalPages}
          </Text>
          {triggerWords.length > 0 && (
            <Text style={styles.triggerInfo}>
              {triggerWords.length} sound triggers found
            </Text>
          )}
          {activeTriggerWords.size > 0 && (
            <Text style={styles.activeTriggers}>
              Playing: {Array.from(activeTriggerWords).join(', ')}
            </Text>
          )}
        </View>

        <TouchableOpacity
          style={[
            styles.navButton,
            (currentChapterIndex === totalChapters - 1 && currentPageIndex === totalPages - 1) && styles.disabledButton
          ]}
          onPress={goToNextPage}
          disabled={currentChapterIndex === totalChapters - 1 && currentPageIndex === totalPages - 1}
        >
          <Text style={styles.navButtonText}>Next</Text>
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
  progressContainer: {
    marginBottom: 16,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    backgroundColor: "#3a3a3a",
  },
  progressText: {
    color: "#ccc",
    fontSize: 12,
    textAlign: "center",
    marginTop: 4,
  },
  headerCard: {
    marginBottom: 16,
    backgroundColor: "#2a2a2a",
  },
  pageContainer: {
    flex: 1,
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
  soundEffectIndicator: {
    color: "#ff6b6b",
    fontSize: 14,
    textAlign: "center",
    marginTop: 10,
  },
  timerButton: {
    marginTop: 10,
    paddingVertical: 8,
    paddingHorizontal: 15,
    backgroundColor: "#4a4a4a",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#fff",
  },
  timerButtonActive: {
    backgroundColor: "#ff6b6b",
    borderColor: "#ff6b6b",
  },
  timerButtonText: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "500",
  },
  triggerInfo: {
    color: "#ccc",
    fontSize: 12,
    marginTop: 8,
  },
  activeTriggers: {
    color: "#ff6b6b",
    fontSize: 12,
    marginTop: 4,
  },
  highlightedWord: {
    backgroundColor: "#ff6b6b",
    padding: 2,
    borderRadius: 4,
  },
}); 