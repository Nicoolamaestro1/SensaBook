import { Stack } from "expo-router";
import { ImageBackground } from "react-native";
import { ThemeProvider, DefaultTheme } from "@react-navigation/native";

const CustomTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

export default function RootLayout() {
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
