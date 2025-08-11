// components/ScreenBackground.tsx
import React from "react";
import { ImageBackground, View, StyleSheet } from "react-native";

export default function ScreenBackground({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ImageBackground
      source={require("../../assets/images/bg-books.jpg")}
      style={styles.bg}
      resizeMode="cover"
    >
      <View style={styles.overlay} />
      {children}
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1, width: "100%", height: "100%" },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.35)", // optional dimmer
  },
});
