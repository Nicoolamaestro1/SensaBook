// CrossPlatformSlider.tsx
import * as React from "react";
import { Platform, View, StyleSheet } from "react-native";
import NativeSlider, { SliderProps } from "@react-native-community/slider";

type Props = Omit<
  SliderProps,
  "onValueChange" | "onSlidingStart" | "onSlidingComplete"
> & {
  value: number | null | undefined;
  onValueChange?: (v: number) => void; // live preview while dragging
  onSlidingStart?: (v: number) => void; // optional
  onSlidingComplete?: (v: number) => void; // commit on release
};

export default function CrossPlatformSlider({
  style,
  value,
  onValueChange,
  onSlidingStart,
  onSlidingComplete,
  minimumValue = 0,
  maximumValue = 1,
  step = 0.01,
  minimumTrackTintColor,
  maximumTrackTintColor,
  thumbTintColor,
  accessibilityLabel,
  disabled,
  ...rest
}: Props) {
  const min = Number(minimumValue);
  const max = Number(maximumValue);
  const stp = Number(step);
  const safeValue = Number.isFinite(Number(value)) ? Number(value) : min;

  // keep the *latest* value for web pointerUp
  const currentRef = React.useRef(safeValue);
  currentRef.current = safeValue;

  const clamp = (n: number) => Math.max(min, Math.min(max, n));

  const handleChange = React.useCallback(
    (n: number) => {
      if (!Number.isFinite(n)) return;
      const clamped = clamp(n);
      currentRef.current = clamped; // keep in sync for web
      if (typeof onValueChange === "function") onValueChange(clamped);
    },
    [onValueChange]
  );

  if (Platform.OS !== "web") {
    return (
      <NativeSlider
        style={style}
        value={safeValue}
        onValueChange={handleChange}
        // ⬇️ pass the live/native value, not safeValue
        onSlidingStart={(n) => onSlidingStart?.(clamp(Number(n)))}
        onSlidingComplete={(n) => onSlidingComplete?.(clamp(Number(n)))}
        minimumValue={min}
        maximumValue={max}
        step={stp}
        minimumTrackTintColor={minimumTrackTintColor}
        maximumTrackTintColor={maximumTrackTintColor}
        thumbTintColor={thumbTintColor}
        accessibilityLabel={accessibilityLabel}
        disabled={disabled}
        {...rest}
      />
    );
  }

  // Web: DOM range input
  const webInputStyle: React.CSSProperties = {
    width: "100%",
    accentColor: minimumTrackTintColor as unknown as string,
  };

  return (
    <View style={[styles.webContainer, style]}>
      <input
        type="range"
        min={min}
        max={max}
        step={stp}
        value={safeValue}
        disabled={!!disabled}
        // keep ref updated + provide live preview
        onChange={(e) => handleChange(Number(e.currentTarget.value))}
        onPointerDown={() => onSlidingStart?.(currentRef.current)}
        // ⬇️ commit the latest value on release
        onPointerUp={(e) =>
          onSlidingComplete?.(clamp(Number(e.currentTarget.value)))
        }
        aria-label={accessibilityLabel}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={safeValue}
        style={webInputStyle}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  webContainer: {
    width: "100%",
    height: 40,
    justifyContent: "center",
  },
});
