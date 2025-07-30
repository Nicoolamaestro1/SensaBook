import { Stack, Tabs } from "expo-router";
import { MaterialCommunityIcons } from "@expo/vector-icons";

export default function RootLayout() {
  return (
    // <Stack>
    //   <Stack.Screen name="index" options={{ headerShown: false}}  />
    // </Stack>
    <Tabs
      screenOptions={{
        headerShown: false,
      }}
    >
      <Tabs.Screen name="index" options={{ headerShown: false, title: "Home", tabBarIcon: ({ color, size }) => (
        <MaterialCommunityIcons name="home" color={color} size={size} />
      ) }} />
      <Tabs.Screen name="profile" options={{ headerShown: false, title: "Profile", tabBarIcon: ({ color, size }) => (
        <MaterialCommunityIcons name="account" color={color} size={size} />
      ) }} />
      <Tabs.Screen name="about" options={{ headerShown: false, title: "About", tabBarIcon: ({ color, size }) => (
        <MaterialCommunityIcons name="information" color={color} size={size} />
      ) }} />
    </Tabs>
  );
}
