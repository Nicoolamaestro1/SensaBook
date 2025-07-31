import * as React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button } from 'react-native-paper';
import { useRouter } from 'expo-router';

export default function LibraryScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text variant="headlineMedium">📚 Welcome to the Library!</Text>
      
      <Button
        mode="contained"
        style={{ marginTop: 20 }}
        onPress={() => router.replace('/')}
      >
        Logout
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
});
