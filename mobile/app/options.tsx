import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { useWpm } from "../hooks/useWpm";
import CrossPlatformSlider from "./components/CrossPlatformSlider";
import ScreenBackground from "./components/ScreenBackground";

export default function OptionsScreen() {
  const { wpm, setWpm } = useWpm();

  return (
    <ScreenBackground>
      <View style={styles.container}>
        <Text style={styles.title}>Reading speed</Text>
        <Text style={styles.value}>{wpm} wpm</Text>

        <CrossPlatformSlider
          minimumValue={50}
          maximumValue={600}
          step={10}
          value={wpm}
          onValueChange={setWpm}
          style={{ width: "100%", height: 40 }}
          minimumTrackTintColor="#5b4636"
          maximumTrackTintColor="#ccc"
          thumbTintColor="#5b4636"
        />

        <View style={styles.scale}>
          <Text>50</Text>
          <Text>600</Text>
        </View>
        <Text style={styles.hint}>
          Tip: 180–250 wpm is comfy for most people.
        </Text>
      </View>
    </ScreenBackground>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  title: { fontSize: 18, fontWeight: "600", marginBottom: 8, color: "#5b4636" },
  value: { fontSize: 24, fontWeight: "700", marginBottom: 12, color: "#fff" },
  scale: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 8,
  },
  hint: { marginTop: 16, color: "#777" },
});
