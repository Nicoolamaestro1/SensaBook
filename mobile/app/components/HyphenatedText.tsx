// components/HyphenatedText.tsx
import React from "react";
import {
  Text,
  StyleSheet,
  Platform,
  type StyleProp,
  type TextStyle,
} from "react-native";

type Props = {
  children: React.ReactNode;
  style?: StyleProp<TextStyle>;
  /** Helps the browser pick the right hyphenation dictionary on web */
  lang?: string; // e.g., 'en', 'de', 'fr'
};

export default function HyphenatedText({
  children,
  style,
  lang = "en",
}: Props) {
  // Extra CSS only on web
  const webHyphenation =
    Platform.OS === "web"
      ? ({
          wordBreak: "break-word",
          overflowWrap: "break-word",
          hyphens: "auto",
        } as React.CSSProperties)
      : null;

  return (
    <Text
      // Compose ONE style prop
      style={[styles.text, style, webHyphenation as any]}
      // RN Web maps this to lang="", which helps hyphenation
      accessibilityLanguage={lang}
    >
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  text: {
    textAlign: "justify",
    // these are defaults; override via `style` when using
    fontSize: 16,
    lineHeight: 24,
  },
});
