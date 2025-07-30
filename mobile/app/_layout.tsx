import * as React from 'react';
import { PaperProvider } from 'react-native-paper';
import LoginScreen from './login';

export default function App() {
  return (
    <PaperProvider>
      <LoginScreen />
    </PaperProvider>
  );
}
