<<<<<<< HEAD
import * as React from 'react';
import { PaperProvider } from 'react-native-paper';
import LoginScreen from './login';

export default function App() {
  return (
    <PaperProvider>
      <LoginScreen />
    </PaperProvider>
=======
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
>>>>>>> main
  );
}
