import * as React from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "reading_wpm";
const DEFAULT_WPM = 200;

export function useWpm() {
  const [wpm, setWpmState] = React.useState<number>(DEFAULT_WPM);

  React.useEffect(() => {
    (async () => {
      try {
        const raw = await AsyncStorage.getItem(KEY);
        if (raw) setWpmState(Math.max(50, Math.min(600, Number(raw))));
      } catch {}
    })();
  }, []);

  const setWpm = React.useCallback(async (val: number) => {
    const clamped = Math.max(50, Math.min(600, Math.round(val)));
    setWpmState(clamped);
    try {
      await AsyncStorage.setItem(KEY, String(clamped));
    } catch {}
  }, []);

  return { wpm, setWpm };
}
