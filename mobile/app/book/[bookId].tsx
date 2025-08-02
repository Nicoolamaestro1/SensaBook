import React from "react";
import { useLocalSearchParams } from "expo-router";
import { View, Text, StyleSheet, ActivityIndicator, ScrollView } from "react-native";
import { Card } from "react-native-paper";
import { Audio } from "expo-av";

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
  const soundRef = React.useRef(null);

  React.useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/books/${bookId}`)
      .then((response) => response.json())
      .then((data) => {
        setBook(data);
        setLoading(false);

        // Fetchuj soundscape za prvu stranu prve glave
        const chapter = data.chapters?.[0];
        const page = chapter?.pages?.[0];
        if (chapter && page) {
          setAudioLoading(true);
          fetch(`http://127.0.0.1:8000/soundscape/book/${bookId}/chapter${chapter.chapter_number}/page/${page.page_number}`)
            .then((res) => res.json())
            .then(async (ss) => {
              let audioModule = null;
              if (ss.carpet_tracks?.length > 0) {
                let track = ss.carpet_tracks[0];
                if (SOUND_MAP[track]) {
                  audioModule = SOUND_MAP[track];
                } else {
                  console.warn("Zvuk nije pronađen u SOUND_MAP:", track);
                }
              }
              if (audioModule) {
                try {
                  const { sound } = await Audio.Sound.createAsync(audioModule);
                  soundRef.current = sound;
                  await sound.playAsync();
                } catch (e) {
                  console.warn("Greška pri puštanju zvuka:", e);
                }
              }
              setAudioLoading(false);
            })
            .catch(() => setAudioLoading(false));
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

  // Uzmi prvu stranu iz prvog poglavlja (ako postoje)
  const firstChapter = book.chapters?.[0];
  const firstPage = firstChapter?.pages?.[0];

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Card style={styles.card}>
        <Card.Title title={book.title} subtitle={book.author} />
        <Card.Content>
          <Text style={styles.summary}>{book.summary}</Text>
          {firstPage ? (
            <>
              <Text style={styles.chapterTitle}>
                {firstChapter?.title
                  ? `Poglavlje: ${firstChapter.title}`
                  : `Poglavlje ${firstChapter?.chapter_number}`}
              </Text>
              <Text style={styles.pageText}>{firstPage.content}</Text>
              {audioLoading && (
                <ActivityIndicator style={{ marginTop: 20 }} size="small" />
              )}
            </>
          ) : (
            <Text style={styles.noPage}>Ova knjiga nema strana.</Text>
          )}
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    alignItems: "center",
    justifyContent: "flex-start",
  },
  card: {
    width: "100%",
    maxWidth: 600,
  },
  summary: {
    marginBottom: 16,
    color: "#fff",
  },
  chapterTitle: {
    marginTop: 16,
    fontWeight: "bold",
    fontSize: 16,
    color: "#fff",
  },
  pageText: {
    marginTop: 8,
    fontSize: 15,
    color: "#fff",
  },
  noPage: {
    marginTop: 16,
    color: "red",
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});
