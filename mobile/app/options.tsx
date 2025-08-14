import React from "react";
import { View, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";
import ScreenBackground from "./components/ScreenBackground";
import ReadingControls from "./components/ReadingControls";
import SoundManager from "./utils/soundManager";
import { useWpm } from "../hooks/useWpm";

// Storage keys
const STORAGE_KEYS = Object.freeze({
  wpm: "settings.wpm",
  ambVol: "settings.ambienceVolPct",
  trigVol: "settings.triggerVolPct",
  fontSize: "settings.fontSizePt",
});

// Bounds used by the slider
const FONT_MIN = 12;
const FONT_MAX = 28;

export default function OptionsScreen() {
  const router = useRouter();
  const { wpm, setWpm } = useWpm();

  const [ambienceVolPct, setAmbienceVolPct] = React.useState(60);
  const [triggerVolPct, setTriggerVolPct] = React.useState(80);
  const [fontSize, setFontSize] = React.useState<number>(16);

  // Load saved values once
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
          const n = clamp01pct(Number(a));
          setAmbienceVolPct(n);
          SoundManager.setCarpetVolume(n / 100);
        }
        if (t) {
          const n = clamp01pct(Number(t));
          setTriggerVolPct(n);
          SoundManager.setTriggerVolume(n / 100);
        }
        if (f) {
          const n = clampFont(Number(f));
          setFontSize(n);
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
          fontSize={fontSize}
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
          onFontSizeChange={(v) => {
            const n = clampFont(v);
            setFontSize(n);
            AsyncStorage.setItem(STORAGE_KEYS.fontSize, String(n)).catch(
              () => {}
            );
          }}
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

function clampFont(n: number) {
  if (!Number.isFinite(n)) return 16;
  return Math.max(FONT_MIN, Math.min(FONT_MAX, Math.round(n)));
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, justifyContent: "center" },
});
