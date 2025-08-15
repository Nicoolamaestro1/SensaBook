// app/wpm-test.tsx
import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Animated,
} from "react-native";
import { useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useWpm } from "../hooks/useWpm"; // ← your existing hook
import { tokenize } from "./utils/reading"; // ← you already export this in reading utils
import { useSafeAreaInsets } from "react-native-safe-area-context";
const COLORS = {
  bg: "#0E0E12",
  card: "#17171c",
  text: "#EAEAF0",
  subtext: "#A6A8B1",
  accent: "#FF7A18",
  border: "rgba(255,255,255,0.06)",
};

const STORAGE_WPM_KEY = "settings.wpm";

// “a couple of seconds” before stop appears — tweak if you like
const STOP_DELAY_MS = 8000; // 8s
// Minimum test duration we’ll accept to avoid nonsense WPM
const MIN_VALID_MS = 5000; // 5s

// ~230–260 words is great.
const TEST_PASSAGE = `
In a small room flooded with morning light, a reader settles into a chair and takes a slow breath before turning the page. 
The world outside grows quieter with each line: traffic blurs, footsteps fade, and the restless hum of distraction begins to soften. 
Words gather like small stones in a riverbed, shaping the flow of attention. 
Some are smooth and familiar, easy to walk across. Others have edges that catch the mind and make it stay a moment longer. 
Reading speed is not a race; it is a rhythm, a conversation between curiosity and clarity. 
When the text invites you forward, you find momentum. When it challenges you, you find presence. 
Neither is better. Both are necessary. 
The point is to arrive—not at the end of a chapter, but at a state of steady focus where the noise recedes and the meaning comes into view. 
As your eyes move, your inner voice keeps time. 
You begin to feel the weight of sentences, the warmth of a well‑placed metaphor, the clean air that follows a good pause. 
With practice, your pace settles into something sustainable—something that carries you without strain. 
This is the speed we want to measure now: your natural reading tempo when you’re attentive but unhurried.
When you’re ready, tap “Start test,” read this passage at your normal pace, and when the “Stop & Set WPM” button appears, press it. 
We’ll calculate your words‑per‑minute from the time you spent reading. 
If your result feels off, you can rerun the test anytime.
`;

export default function WpmTestScreen() {
  const router = useRouter();
  const { setWpm } = useWpm();

  const [startedAt, setStartedAt] = React.useState<number | null>(null);
  const [canStop, setCanStop] = React.useState(false);
  const [finished, setFinished] = React.useState(false);
  const insets = useSafeAreaInsets();

  const startFade = React.useRef(new Animated.Value(1)).current;

  const totalWords = React.useMemo(() => tokenize(TEST_PASSAGE).length, []);

  const handleStart = React.useCallback(() => {
    // fade out the start button
    Animated.timing(startFade, {
      toValue: 0,
      duration: 350,
      useNativeDriver: true,
    }).start();
    setStartedAt(Date.now());
    // allow stopping after a short delay
    setTimeout(() => setCanStop(true), STOP_DELAY_MS);
  }, [startFade]);

  const clamp = (n: number, lo: number, hi: number) =>
    Math.max(lo, Math.min(hi, n));

  const handleStopAndSet = React.useCallback(async () => {
    if (!startedAt) return;
    const elapsedMs = Date.now() - startedAt;
    setFinished(true);

    if (elapsedMs < MIN_VALID_MS) {
      // too short → show a gentle nudge and reset
      alert(
        "That was too quick to measure accurately. Try reading for at least 5 seconds."
      );
      setStartedAt(null);
      setCanStop(false);
      startFade.setValue(1);
      return;
    }

    // WPM = words read / minutes spent.
    // We assume the passage was read during the measured time.
    const minutes = elapsedMs / 60000;
    const rawWpm = Math.round(totalWords / minutes);
    const safeWpm = clamp(rawWpm, 50, 600);
    setWpm(safeWpm);
    await AsyncStorage.setItem(STORAGE_WPM_KEY, String(safeWpm));

    // Send them to the library (or wherever you want next)
    router.replace("/library");
  }, [startedAt, totalWords, setWpm, router, startFade]);

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.pageCard}>
        <Text style={styles.chapterTitle}>Reading Speed Test</Text>
        <Text style={styles.subtext}>
          Read the passage below at your normal pace. We’ll set your WPM
          automatically.
        </Text>

        <ScrollView
          style={styles.passageWrap}
          contentContainerStyle={{ paddingBottom: 24 }}
          showsVerticalScrollIndicator={false}
        >
          <Text style={styles.pageText}>{TEST_PASSAGE}</Text>
        </ScrollView>

        {/* Start button (fades out) */}
        {!startedAt && (
          <Animated.View style={{ opacity: startFade }}>
            <TouchableOpacity style={styles.primaryBtn} onPress={handleStart}>
              <Text style={styles.primaryBtnText}>Start test</Text>
            </TouchableOpacity>
          </Animated.View>
        )}

        {/* Stop button (appears after a delay) */}
        {startedAt && canStop && !finished && (
          <TouchableOpacity style={styles.stopBtn} onPress={handleStopAndSet}>
            <Text style={styles.stopBtnText}>Stop & Set WPM</Text>
          </TouchableOpacity>
        )}

        {/* Disabled (waiting) indicator */}
        {startedAt && !canStop && !finished && (
          <Text style={styles.waitingText}>
            Keep reading… button will appear soon
          </Text>
        )}

        {/* Retry if needed */}
        {finished && (
          <TouchableOpacity
            style={[styles.primaryBtn, { borderColor: "#fff", marginTop: 10 }]}
            onPress={() => {
              setFinished(false);
              setStartedAt(null);
              setCanStop(false);
              startFade.setValue(1);
            }}
          >
            <Text style={styles.primaryBtnText}>Rerun test</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  // Same container spacing as Book page
  container: {
    flex: 1,
    padding: 16,
    paddingTop: 0,
    position: "relative",
    backgroundColor: "rgb(245, 236, 217))",
  },

  // Transparent card like Book page
  pageCard: { flex: 1, backgroundColor: "transparent", marginBottom: 16 },

  // Title matches chapterTitle in Book page
  chapterTitle: {
    marginTop: 16,
    fontWeight: "bold",
    fontSize: 18,
    color: "#5b4636",
    marginBottom: 8,
  },

  // Subtitle matches your text tone
  subtext: {
    fontSize: 14,
    color: "#5b4636",
    marginBottom: 12,
    opacity: 0.95,
  },

  // Body text exactly like pageText
  pageText: {
    color: "#5b4636",
    textAlign: "justify",
    fontSize: 16,
    lineHeight: 24,
  },

  // Keep scroll container simple/transparent like reader
  passageWrap: { backgroundColor: "transparent", marginBottom: 16, flex: 1 },

  // Primary button identical to Book page primaryBtn
  primaryBtn: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "transparent",
    paddingVertical: 14,
    borderWidth: 1,
    borderColor: "#000",
    borderRadius: 50,
    marginTop: 8,
    marginBottom: 16,
    alignSelf: "center",
  },
  primaryBtnText: {
    textAlign: "center",
    color: "#000",
    fontSize: 16,
    fontWeight: "600",
    fontFamily: "Montserrat_700Bold",
  },

  // Stop button: keep shape/size, use your accent fill
  stopBtn: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "#FF7A18",
    paddingVertical: 14,
    borderRadius: 50,
    alignSelf: "center",
    marginTop: 0,
    marginBottom: 16,
  },
  stopBtnText: {
    textAlign: "center",
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
    fontFamily: "Montserrat_700Bold",
  },

  // Waiting line styled like your page text
  waitingText: {
    textAlign: "center",
    color: "#5b4636",
    fontSize: 14,
    marginTop: 8,
  },
});
