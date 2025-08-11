import React from "react";
import { Stack } from "expo-router";
import {
  ImageBackground,
  ActivityIndicator,
  View,
  StyleSheet, // ✅ add this
} from "react-native";
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
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

export default function RootLayout() {
  const [fontsLoaded] = useFonts({
    Montserrat_300Light,
    Montserrat_400Regular,
    Montserrat_500Medium,
    Montserrat_700Bold,
  });

  if (!fontsLoaded) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <ImageBackground
      source={require("../assets/images/bg-books.jpg")}
      style={styles.bg}
      resizeMode="cover"
    >
      {/* optional dim overlay for readability */}
      <View
        pointerEvents="none"
        style={[
          StyleSheet.absoluteFillObject,
          { backgroundColor: "rgba(0,0,0,0.35)" },
        ]}
      />

      <ThemeProvider value={CustomTheme}>
        <Stack
          screenOptions={{
            headerShown: false,
            contentStyle: { backgroundColor: "transparent" }, // let bg show
            animation: "fade", // smoother with transparent roots
            freezeOnBlur: true,
            // detachPreviousScreen: true, // ❌ avoid with transparent backgrounds
          }}
        />
      </ThemeProvider>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1, width: "100%", height: "100%" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
});
