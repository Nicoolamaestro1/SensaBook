// app/options.tsx (or wherever your screen lives)
import React from "react";
import { View, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";
import ScreenBackground from "./components/ScreenBackground";
import ReadingControls from "./components/ReadingControls";
import SoundManager from "./utils/soundManager";
import { useWpm } from "../hooks/useWpm";

// Re‑use the same storage keys the reader uses
const STORAGE_KEYS = Object.freeze({
  wpm: "settings.wpm",
  ambVol: "settings.ambienceVolPct",
  trigVol: "settings.triggerVolPct",
});

export default function OptionsScreen() {
  const router = useRouter();
  const { wpm, setWpm } = useWpm();
  const [ambienceVolPct, setAmbienceVolPct] = React.useState(60);
  const [triggerVolPct, setTriggerVolPct] = React.useState(80);

  // Load saved values once
  React.useEffect(() => {
    (async () => {
      try {
        const [w, a, t] = await Promise.all([
          AsyncStorage.getItem(STORAGE_KEYS.wpm),
          AsyncStorage.getItem(STORAGE_KEYS.ambVol),
          AsyncStorage.getItem(STORAGE_KEYS.trigVol),
        ]);
        if (w) setWpm(Math.max(50, Math.min(600, Number(w))));
        if (a) {
          const n = clamp01pct(Number(a));
          setAmbienceVolPct(n);
          SoundManager.setCarpetVolume(n / 100);
        }
        if (t) {
          const n = clamp01pct(Number(t));
          setTriggerVolPct(n);
          SoundManager.setTriggerVolume(n / 100);
        }
      } catch {
        // ignore
      }
    })();
  }, [setWpm]);

  return (
    <ScreenBackground>
      <View style={styles.container}>
        <ReadingControls
          wpm={wpm}
          ambienceVolPct={ambienceVolPct}
          triggerVolPct={triggerVolPct}
          onWpmChange={(v) => {
            setWpm(v);
            AsyncStorage.setItem(STORAGE_KEYS.wpm, String(v)).catch(() => {});
          }}
          onAmbienceChange={(v) => {
            const n = clamp01pct(v);
            setAmbienceVolPct(n);
            SoundManager.setCarpetVolume(n / 100);
            AsyncStorage.setItem(STORAGE_KEYS.ambVol, String(n)).catch(
              () => {}
            );
          }}
          onTriggerChange={(v) => {
            const n = clamp01pct(v);
            setTriggerVolPct(n);
            SoundManager.setTriggerVolume(n / 100);
            AsyncStorage.setItem(STORAGE_KEYS.trigVol, String(n)).catch(
              () => {}
            );
          }}
          // Optional actions for the two buttons in the component:
          onBackToLibrary={() => {
            router.replace("/library");
          }}
          hideClose
        />
      </View>
    </ScreenBackground>
  );
}

function clamp01pct(n: number) {
  if (Number.isNaN(n)) return 0;
  return Math.max(0, Math.min(100, Math.round(n)));
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, justifyContent: "center" },
});
