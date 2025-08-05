import React from "react";
import { Stack } from "expo-router";
import { ImageBackground, ActivityIndicator, View } from "react-native";
import { ThemeProvider, DefaultTheme } from "@react-navigation/native";
import {
  useFonts,
  Montserrat_400Regular,
  Montserrat_700Bold,
} from "@expo-google-fonts/montserrat";

const CustomTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

export default function RootLayout() {
  const [fontsLoaded] = useFonts({
    Montserrat_400Regular,
    Montserrat_700Bold,
  });

  if (!fontsLoaded) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <ImageBackground
      source={require("../assets/images/bg-books.jpg")}
      style={{ flex: 1, width: "100%", height: "100%" }}
      resizeMode="cover"
    >
      <ThemeProvider value={CustomTheme}>
        <Stack screenOptions={{ headerShown: false }} />
      </ThemeProvider>
    </ImageBackground>
  );
}
