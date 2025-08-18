import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Pressable,
} from "react-native";
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
  fontSize: number;
  onWpmChange: (v: number) => void;
  onAmbienceChange: (v: number) => void;
  onTriggerChange: (v: number) => void;
  onFontSizeChange: (v: number) => void;
  onBackToLibrary?: () => void;
  onAnySliderStart?: () => void;
  onAnySliderEnd?: () => void;
  onClose?: () => void;
  hideClose?: boolean;
  colors?: Partial<typeof DEFAULT_COLORS>;
};

const WPM_MIN = 50;
const WPM_MAX = 600;
const FONT_MIN = 12;
const FONT_MAX = 28;
const VOL_MIN = 0;
const VOL_MAX = 100;

export default function ReadingControls({
  wpm,
  ambienceVolPct,
  triggerVolPct,
  fontSize,
  onWpmChange,
  onAmbienceChange,
  onTriggerChange,
  onFontSizeChange,
  onBackToLibrary,
  onClose,
  hideClose = false,
  onAnySliderStart,
  onAnySliderEnd,
  colors = {},
}: Props) {
  const c = { ...DEFAULT_COLORS, ...colors };

  // local preview state while sliding
  const [wpmLocal, setWpmLocal] = React.useState(wpm);
  const [fontLocal, setFontLocal] = React.useState(fontSize);
  const [ambLocal, setAmbLocal] = React.useState(ambienceVolPct);
  const [trigLocal, setTrigLocal] = React.useState(triggerVolPct);

  // keep locals in sync if parent updates from elsewhere
  React.useEffect(() => setWpmLocal(wpm), [wpm]);
  React.useEffect(() => setFontLocal(fontSize), [fontSize]);
  React.useEffect(() => setAmbLocal(ambienceVolPct), [ambienceVolPct]);
  React.useEffect(() => setTrigLocal(triggerVolPct), [triggerVolPct]);

  const clamp = (n: number, lo: number, hi: number) =>
    Math.max(lo, Math.min(hi, n));

  return (
    <View style={{ width: "100%" }}>
      <Text style={[styles.panelTitle, { color: c.text }]}>Options</Text>

      {/* WPM */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>Reading speed</Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>
        {wpmLocal} wpm
      </Text>
      <CrossPlatformSlider
        testID="slider:wpm"
        minimumValue={WPM_MIN}
        maximumValue={WPM_MAX}
        step={10}
        value={wpmLocal}
        onSlidingStart={() => onAnySliderStart?.()}
        onValueChange={(v) =>
          setWpmLocal(clamp(Math.round(v), WPM_MIN, WPM_MAX))
        }
        onSlidingComplete={(v) => {
          onWpmChange(clamp(Math.round(v), WPM_MIN, WPM_MAX));
          onAnySliderEnd?.(); // ⬅️ end
        }}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{WPM_MIN}</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{WPM_MAX}</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Tip: 180–250 wpm is comfy for most people.
      </Text>

      <View style={styles.horizontalLine} />

      {/* Font Size */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>Font size</Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>
        {fontLocal} pt
      </Text>
      <CrossPlatformSlider
        testID="slider:fontSize"
        value={fontLocal}
        minimumValue={FONT_MIN}
        maximumValue={FONT_MAX}
        step={1}
        onSlidingStart={() => onAnySliderStart?.()}
        onValueChange={(v) =>
          setFontLocal(clamp(Math.round(v), FONT_MIN, FONT_MAX))
        }
        onSlidingComplete={(v) => {
          onFontSizeChange(clamp(Math.round(v), FONT_MIN, FONT_MAX));
          onAnySliderEnd?.();
        }}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
        accessibilityLabel="Font size slider"
      />
      <View style={[styles.sliderScale, { alignItems: "flex-end" }]}>
        <Text style={{ color: c.subtext, fontSize: 12, lineHeight: 16 }}>
          A
        </Text>
        <Text style={{ color: c.subtext, fontSize: 22, lineHeight: 24 }}>
          A
        </Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Affects the size of book text.
      </Text>

      <View style={styles.horizontalLine} />

      {/* Ambience */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>
        Ambience volume
      </Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>{ambLocal}%</Text>
      <CrossPlatformSlider
        testID="slider:ambience"
        minimumValue={VOL_MIN}
        maximumValue={VOL_MAX}
        step={1}
        value={ambLocal}
        onSlidingStart={() => onAnySliderStart?.()}
        onValueChange={(v) =>
          setAmbLocal(clamp(Math.round(v), VOL_MIN, VOL_MAX))
        }
        onSlidingComplete={(v) => {
          onAmbienceChange(clamp(Math.round(v), VOL_MIN, VOL_MAX));
          onAnySliderEnd?.();
        }}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{VOL_MIN}</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{VOL_MAX}</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Controls the background ambience (loops).
      </Text>

      <View style={styles.horizontalLine} />

      {/* Triggers */}
      <Text style={[styles.sliderTitle, { color: c.text }]}>
        Trigger volume
      </Text>
      <Text style={[styles.sliderValue, { color: c.accent }]}>
        {trigLocal}%
      </Text>
      <CrossPlatformSlider
        testID="slider:trigger"
        minimumValue={VOL_MIN}
        maximumValue={VOL_MAX}
        step={1}
        value={trigLocal}
        onSlidingStart={() => onAnySliderStart?.()}
        onValueChange={(v) =>
          setTrigLocal(clamp(Math.round(v), VOL_MIN, VOL_MAX))
        }
        onSlidingComplete={(v) => {
          onTriggerChange(clamp(Math.round(v), VOL_MIN, VOL_MAX));
          onAnySliderEnd?.();
        }}
        minimumTrackTintColor={c.accent}
        maximumTrackTintColor="rgba(255,255,255,0.2)"
        thumbTintColor={c.accent}
      />
      <View style={styles.sliderScale}>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{VOL_MIN}</Text>
        <Text style={[styles.scaleText, { color: c.subtext }]}>{VOL_MAX}</Text>
      </View>
      <Text style={[styles.sliderHint, { color: c.subtext }]}>
        Controls one-shot sound effects on trigger words.
      </Text>

      <View style={styles.horizontalLine} />

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

      {/* Close */}
      {!hideClose && onClose && (
        <Pressable
          onPress={onClose}
          hitSlop={{ top: 12, bottom: 12, left: 16, right: 16 }}
          style={({ pressed }) => [
            {
              alignSelf: "center",
              marginTop: 8,
              paddingHorizontal: 16,
              paddingVertical: 10,
              borderRadius: 20,
              opacity: pressed ? 0.6 : 1,
            },
          ]}
          accessibilityRole="button"
          accessibilityLabel="Close options"
        >
          <Text
            style={{ color: c.accent, fontWeight: "600", textAlign: "center" }}
          >
            Close
          </Text>
        </Pressable>
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
    fontFamily: "Montserrat_700Bold",
  },
  horizontalLine: {
    width: "100%",
    height: 1,
    backgroundColor: "#eee",
    opacity: 0.7,
    marginTop: 15,
    marginBottom: 15,
    alignSelf: "stretch",
  },
});
