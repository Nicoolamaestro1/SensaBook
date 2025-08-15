import * as React from "react";
import { Platform, View, StyleSheet } from "react-native";
import NativeSlider, { SliderProps } from "@react-native-community/slider";

type Props = Omit<
  SliderProps,
  "onValueChange" | "onSlidingStart" | "onSlidingComplete"
> & {
  value: number | null | undefined;
  onValueChange?: (v: number) => void; // defensive: optional at runtime
  onSlidingStart?: (v: number) => void;
  onSlidingComplete?: (v: number) => void;
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

  const handleChange = React.useCallback(
    (n: number) => {
      if (typeof onValueChange === "function") onValueChange(n);
      else if (__DEV__) {
        const name =
          (rest as any)?.accessibilityLabel ||
          (rest as any)?.testID ||
          "CrossPlatformSlider";
        console.warn(`[${name}] onValueChange missing; value=${n}`);
      }
    },
    [onValueChange, rest]
  );

  if (Platform.OS !== "web") {
    return (
      <NativeSlider
        style={style}
        value={safeValue}
        onValueChange={handleChange}
        onSlidingStart={() => onSlidingStart?.(safeValue)}
        onSlidingComplete={() => onSlidingComplete?.(safeValue)}
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

  // Web: DOM range input with proper CSSProperties (don’t pass RN styles)
  const webInputStyle: React.CSSProperties = {
    width: "100%",
    // Modern browsers: accentColor maps to active track + thumb
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
        onChange={(e) => handleChange(Number(e.currentTarget.value))}
        onPointerDown={() => onSlidingStart?.(safeValue)}
        onPointerUp={() => onSlidingComplete?.(safeValue)}
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
  webContainer: { width: "100%", height: 40, justifyContent: "center" },
});
