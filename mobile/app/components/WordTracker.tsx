// components/WordTracker.tsx
import * as React from "react";
import { View, StyleSheet, LayoutChangeEvent } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  runOnJS,
} from "react-native-reanimated";

type Props = {
  width: number;
  activeIndex: number; // current word from parent when NOT dragging
  totalWords: number;
  marks: number[]; // normalized [0..1] tick positions for triggers
  triggerSet?: Set<number>; // to glow thumb when on a trigger
  onSeekStart: () => void;
  onSeekEnd: (index: number) => void;
};

export const WordTracker = React.memo(function WordTracker({
  width,
  activeIndex,
  totalWords,
  marks,
  triggerSet,
  onSeekStart,
  onSeekEnd,
}: Props) {
  const [layoutW, setLayoutW] = React.useState(0);
  const wJS = layoutW || width || 1;

  // shared values so UI updates don't re-render React tree
  const w = useSharedValue(1);
  const progress = useSharedValue(0); // 0..1
  const dragging = React.useRef(false);
  const [dragIdx, setDragIdx] = React.useState<number | null>(null);

  const denom = Math.max(1, totalWords - 1);
  const idxToProgress = (idx: number) =>
    totalWords > 1 ? Math.min(1, Math.max(0, idx / denom)) : 0;

  // Sync to parent while NOT dragging
  React.useEffect(() => {
    if (dragging.current) return;
    progress.value = withTiming(idxToProgress(activeIndex), { duration: 80 });
  }, [activeIndex, totalWords]); // eslint-disable-line react-hooks/exhaustive-deps

  // keep shared width in sync
  const onLayout = (e: LayoutChangeEvent) => {
    const ww = e.nativeEvent.layout.width || width || 1;
    setLayoutW(ww);
    w.value = ww;
  };

  // styles that run on the UI thread
  const fillStyle = useAnimatedStyle(() => ({
    width: w.value * progress.value,
  }));
  const thumbStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: Math.max(0, w.value * progress.value - 6) }],
  }));

  // helpers
  const xToIndex = React.useCallback(
    (x: number) => {
      const clamped = Math.max(0, Math.min(wJS, x));
      const frac = clamped / wJS;
      return Math.round(frac * Math.max(0, totalWords - 1));
    },
    [wJS, totalWords]
  );

  // Responder handlers (no RNGH, very stable in Expo Go)
  const grant = (e: any) => {
    dragging.current = true;
    onSeekStart();
    const idx = xToIndex(e.nativeEvent.locationX);
    setDragIdx(idx); // local re-render only
    progress.value = idxToProgress(idx);
  };

  const move = (e: any) => {
    const idx = xToIndex(e.nativeEvent.locationX);
    setDragIdx(idx);
    progress.value = idxToProgress(idx);
  };

  const release = (e: any) => {
    const idx = xToIndex(e.nativeEvent.locationX);
    dragging.current = false;
    setDragIdx(null);
    progress.value = withTiming(idxToProgress(idx), { duration: 80 });
    runOnJS(onSeekEnd)(idx);
  };

  const isOnTriggerNow =
    (dragIdx != null && triggerSet?.has(dragIdx)) ||
    (dragIdx == null && triggerSet?.has(activeIndex));

  return (
    <View
      style={[styles.container, { width }]}
      onLayout={onLayout}
      onStartShouldSetResponder={() => true}
      onMoveShouldSetResponder={() => true}
      onResponderGrant={grant}
      onResponderMove={move}
      onResponderRelease={release}
      onResponderTerminationRequest={() => false}
      pointerEvents="box-only"
    >
      <View style={styles.track}>
        {/* progress fill */}
        <Animated.View style={[styles.fill, fillStyle]} />

        {/* ticks */}
        {marks.map((m, i) => (
          <View
            key={i}
            style={[styles.tick, { left: wJS * m - 0.5 }]}
            pointerEvents="none"
          />
        ))}

        {/* thumb */}
        <Animated.View
          style={[
            styles.thumb,
            thumbStyle,
            isOnTriggerNow ? styles.thumbTrigger : null,
          ]}
          pointerEvents="none"
        />
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    marginTop: 8,
    alignSelf: "stretch",
    height: 18,
    justifyContent: "center",
  },
  track: {
    height: 4,
    borderRadius: 2,
    backgroundColor: "rgba(31,25,15,0.12)",
    overflow: "hidden",
  },
  fill: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    borderRadius: 2,
    backgroundColor: "rgba(31,25,15,0.45)",
  },
  tick: {
    position: "absolute",
    top: -2,
    width: 1,
    height: 8,
    backgroundColor: "rgba(31,25,15,0.5)",
  },
  thumb: {
    position: "absolute",
    top: -4,
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#1F190F",
    opacity: 0.7,
  },
  thumbTrigger: {
    backgroundColor: "#C08C2B",
    opacity: 1,
  },
});
