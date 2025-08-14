// app/components/ReadingControls.tsx
import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import CrossPlatformSlider from "./CrossPlatformSlider";

const DEFAULT_COLORS = {
  text: "#EAEAF0",
  subtext: "#A6A8B1",
  accent: "#FF7A18",
};

type Props = {
  wpm: number;
  ambienceVolPct: number;
  triggerVolPct: number;
  onWpmChange: (v: number) => void;
  onAmbienceChange: (v: number) => void;
  onTriggerChange: (v: number) => void;
  onBackToLibrary?: () => void;
  onClose?: () => void;
  hideClose?: boolean;
  colors?: Partial<typeof DEFAULT_COLORS>;
};

export default function ReadingControls({
  wpm,
  ambienceVolPct,
  triggerVolPct,
  onWpmChange,
  onAmbienceChange,
  onTriggerChange,
  onBackToLibrary,
  onClose,
  hideClose = false,
  colors = {},
}: Props) {
  const c = { ...DEFAULT_COLORS, ...colors };

  return (
    <View>
      <Text style={[styles.panelTitle, { color: c.text }]}>Options</Text>

      {/* WPM */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>Reading speed</Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>{wpm} wpm</Text>
      <CrossPlatformSlider
        minimumValue={50}
        maximumValue={600}
        step={10}
        value={wpm}
        onValueChange={onWpmChange}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>50</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>600</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Tip: 180–250 wpm is comfy for most people.
      </Text>

      {/* Ambience */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>
        Ambience volume
      </Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>
        {ambienceVolPct}%
      </Text>
      <CrossPlatformSlider
        minimumValue={0}
        maximumValue={100}
        step={1}
        value={ambienceVolPct}
        onValueChange={onAmbienceChange}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>0</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>100</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Controls the background ambience (loops).
      </Text>

      {/* Triggers */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>
        Trigger volume
      </Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>
        {triggerVolPct}%
      </Text>
      <CrossPlatformSlider
        minimumValue={0}
        maximumValue={100}
        step={1}
        value={triggerVolPct}
        onValueChange={onTriggerChange}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>0</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>100</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Controls one‑shot sound effects on trigger words.
      </Text>

      {onBackToLibrary && (
        <TouchableOpacity
          onPress={onBackToLibrary}
          style={[styles.primaryBtn, { borderColor: c.text }]}
        >
          <Text style={[styles.primaryBtnText, { color: c.text }]}>
            Back to Library
          </Text>
        </TouchableOpacity>
      )}

      {!hideClose && onClose && (
        <TouchableOpacity onPress={onClose} style={{ marginTop: 8 }}>
          <Text
            style={{ color: c.accent, fontWeight: "600", textAlign: "center" }}
          >
            Close
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  panelTitle: { fontWeight: "800", fontSize: 20, marginBottom: 8 },
  sliderTitle: { fontSize: 16, fontWeight: "700", marginBottom: 6 },
  sliderValue: { fontSize: 28, fontWeight: "800", marginBottom: 10 },
  sliderScale: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 6,
  },
  scaleText: {},
  sliderHint: { fontSize: 12, marginTop: 6, marginBottom: 16 },
  primaryBtn: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "transparent",
    paddingVertical: 14,
    borderWidth: 1,
    borderRadius: 50,
    marginTop: 8,
    marginBottom: 16,
    alignSelf: "center",
  },
  primaryBtnText: {
    textAlign: "center",
    fontSize: 16,
    fontWeight: "600",
  },
});
