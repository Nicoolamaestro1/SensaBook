// app/_layout.tsx
import React from "react";
import { Stack } from "expo-router";
import { ThemeProvider, DefaultTheme } from "@react-navigation/native";
import {
  useFonts,
  Montserrat_300Light,
  Montserrat_400Regular,
  Montserrat_500Medium,
  Montserrat_700Bold,
} from "@expo-google-fonts/montserrat";

const CustomTheme = {
  ...DefaultTheme,
  colors: { ...DefaultTheme.colors, background: "#0d0b1a" }, // opaque
};

export default function RootLayout() {
  const [fontsLoaded] = useFonts({
    Montserrat_300Light,
    Montserrat_400Regular,
    Montserrat_500Medium,
    Montserrat_700Bold,
  });

  return (
    <ThemeProvider value={CustomTheme}>
      <Stack
        screenOptions={{
          headerShown: false,
          animation: "slide_from_right",
          contentStyle: { backgroundColor: "#0d0b1a" }, // opaque screen view
        }}
      />
    </ThemeProvider>
  );
}
