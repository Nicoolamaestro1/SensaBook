import * as React from "react";
import { Platform, View, StyleSheet } from "react-native";
import NativeSlider from "@react-native-community/slider";

type Props = {
  value: number;
  onValueChange: (v: number) => void;
  minimumValue?: number;
  maximumValue?: number;
  step?: number;
  style?: any;
  minimumTrackTintColor?: string;
  maximumTrackTintColor?: string;
  thumbTintColor?: string;
  onSlidingStart?: () => void;
  onSlidingComplete?: () => void;
  disabled?: boolean;
};

export default function CrossPlatformSlider(props: Props) {
  if (Platform.OS !== "web") {
    return <NativeSlider {...props} />;
  }

  const {
    value,
    onValueChange,
    minimumValue = 0,
    maximumValue = 1,
    step = 0.01,
    onSlidingStart,
    onSlidingComplete,
    disabled,
    style,
  } = props;

  return (
    <View style={[styles.webContainer, style]}>
      <input
        type="range"
        min={minimumValue}
        max={maximumValue}
        step={step}
        value={value}
        disabled={disabled}
        onChange={(e) => onValueChange?.(Number(e.target.value))}
        onMouseDown={onSlidingStart}
        onTouchStart={onSlidingStart}
        onMouseUp={onSlidingComplete}
        onTouchEnd={onSlidingComplete}
        style={styles.webInput as any}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  webContainer: { width: "100%", height: 40, justifyContent: "center" },
  webInput: { width: "100%" },
});