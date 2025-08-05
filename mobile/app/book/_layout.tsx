import { Stack } from "expo-router";
import { View } from "react-native";
import { ThemeProvider, DefaultTheme } from "@react-navigation/native";

const CustomTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

export default function BookLayout() {
  return (
    <View
      style={{ flex: 1, width: "100%", height: "100%", backgroundColor: "#f5ecd9" }} 
    >
      <ThemeProvider value={CustomTheme}>
        <Stack screenOptions={{ headerShown: false }} />
      </ThemeProvider>
    </View>
  );
}
