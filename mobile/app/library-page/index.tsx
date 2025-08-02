import * as React from 'react';
import { View, StyleSheet, FlatList, Dimensions, TouchableOpacity } from 'react-native';
import { Text, Button, Card, ActivityIndicator } from 'react-native-paper';
import { useRouter } from 'expo-router';

export default function LibraryScreen() {
  const router = useRouter();
  const [books, setBooks] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [numColumns, setNumColumns] = React.useState(1);

  React.useEffect(() => {
    fetch('http://127.0.0.1:8000/api/books')
      .then((response) => response.json())
      .then((data) => {
        setBooks(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  React.useEffect(() => {
    const updateColumns = () => {
      const width = Dimensions.get('window').width;
      if (width < 600) setNumColumns(1);
      else if (width < 900) setNumColumns(2);
      else setNumColumns(3);
    };
    updateColumns();
    const subscription = Dimensions.addEventListener('change', updateColumns);
    return () => subscription?.remove();
  }, []);

  return (
    <View style={styles.container}>
      <Text variant="headlineMedium" style={{ marginBottom: 24 }}>📚 Welcome to the Library!</Text>
      {loading ? (
        <ActivityIndicator style={{ marginTop: 24 }} animating size="large" />
      ) : (
        <FlatList
          contentContainerStyle={styles.row}
          data={books}
          keyExtractor={(item) => item.id.toString()}
          numColumns={numColumns}
          renderItem={({ item }) => (
            <View style={[styles.cardWrapper, { flex: 1 / numColumns }]}>
              <TouchableOpacity
                style={{ flex: 1 }}
                onPress={() => router.push(`/book/${item.id}`)}
                activeOpacity={0.85}
              >
                <Card style={styles.card}>
                  <Card.Title title={item.title} subtitle={item.author} />
                  <Card.Content>
                    <Text style={{ fontSize: 12 }}>{item.summary || 'No description.'}</Text>
                  </Card.Content>
                </Card>
              </TouchableOpacity>
            </View>
          )}
          ListEmptyComponent={
            <Text style={{ textAlign: 'center', marginTop: 16 }}>
              No books found.
            </Text>
          }
        />
      )}
      <Button
        mode="contained"
        style={{ marginTop: 32, marginBottom: 24 }}
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
    paddingTop: 24,
    alignItems: "center",
    backgroundColor: "#fff",
    paddingBottom: 64,
  },
  row: {
    alignItems: "flex-start",
    paddingHorizontal: 8,
    paddingBottom: 16,
  },
  cardWrapper: {
    padding: 8,
    minWidth: 220,
    maxWidth: 400,
  },
  card: {
    flex: 1,
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#35333A',
  },
});
