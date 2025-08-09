import React from "react";
import { View, Text, StyleSheet, Animated, Easing, Pressable } from "react-native";
import CrossPlatformSlider from "../components/CrossPlatformSlider";
import { useWpm } from "../../hooks/useWpm";

type Props = {
  visible: boolean;
  onClose: () => void;
};

export default function TopOptionsSheet({ visible, onClose }: Props) {
  const { wpm, setWpm } = useWpm();
  const height = 220;
  const anim = React.useRef(new Animated.Value(-height)).current;

  React.useEffect(() => {
    Animated.timing(anim, {
      toValue: visible ? 0 : -height,
      duration: 220,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: true,
    }).start();
  }, [visible]);

  return (
    <>
      {/* dim background, only when visible */}
      {visible && (
        <Pressable style={StyleSheet.absoluteFill} onPress={onClose} />
      )}

      <Animated.View
        pointerEvents={visible ? "auto" : "none"}
        style={[
          styles.sheet,
          { transform: [{ translateY: anim }], height },
        ]}
      >
        <View style={styles.header}>
          <Text style={styles.title}>Options</Text>
          <Pressable onPress={onClose}><Text style={styles.close}>Close</Text></Pressable>
        </View>

        <View style={{ marginTop: 12 }}>
          <Text style={styles.label}>Reading speed</Text>
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
        </View>
      </Animated.View>
    </>
  );
}

const styles = StyleSheet.create({
  sheet: {
    position: "absolute",
    left: 0,
    right: 0,
    top: 0,
    backgroundColor: "white",
    padding: 16,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    shadowColor: "#000",
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 6,
    zIndex: 30,
  },
  header: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  title: { fontSize: 16, fontWeight: "700", color: "#5b4636" },
  close: { color: "#5b4636", fontWeight: "600" },
  label: { color: "#5b4636", fontWeight: "600" },
  value: { marginBottom: 8, fontWeight: "700" },
});
