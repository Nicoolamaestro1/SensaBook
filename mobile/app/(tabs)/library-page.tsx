import * as React from 'react';
import { View, Image, StyleSheet, FlatList, Dimensions, TouchableOpacity, Text, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';

export default function LibraryScreen() {
  const router = useRouter();
  const [books, setBooks] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState(true);


  React.useEffect(() => {
    fetch('http://127.0.0.1:8000/api/books')
      .then((response) => response.json())
      .then((data) => {
        setBooks(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>📚 Welcome to the Library!</Text>

      {loading ? (
        <ActivityIndicator style={{ marginTop: 24 }} size="large" color="#2563eb" />
      ) : (
        <FlatList
          contentContainerStyle={styles.row}
          data={books}
          keyExtractor={(item) => item.id.toString()}
          numColumns={3}
          key={3} 
          renderItem={({ item }) => (
            <View style={[styles.cardWrapper, { flex: 1 / 3 }]}>
              <TouchableOpacity
                style={styles.card}
                onPress={() => router.push(`/book/${item.id}`)}
                activeOpacity={0.85}
              >
                {item.cover_url ? (
                  <Image
                    source={{ uri: item.cover_url }}
                    style={styles.cardImage}
                    resizeMode="cover"
                  />
                ) : null}
                <Text style={styles.cardTitle}>{item.title}</Text>
                <Text style={styles.cardSubtitle}>{item.author}</Text>
              </TouchableOpacity>
            </View>
          )}
          ListEmptyComponent={
            <Text style={{ textAlign: 'center', color: "#fff", marginTop: 16 }}>
              No books found.
            </Text>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
     flex: 1,
    alignSelf: "center",
    width: "100%",
    maxWidth: 1200,
  },
  heading: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 24,
    marginTop: 24,
    textAlign: "center",
    color: "#fff"
  },
  row: {
    paddingHorizontal: 8,
    paddingBottom: 16,
    marginBottom: 30
  },
  cardWrapper: {
    flex: 1,
    padding: 10,
  },
  card: {
    height: "100%",
    borderRadius: 12,
    padding: 0,
    shadowOpacity: 0.1,
    elevation: 2,
  },
  cardImage: {
    width: "100%",
    aspectRatio: 1 / 1, 
    borderRadius: 8,
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 4,
    paddingHorizontal: 16,
    textAlign: "center",
    color: "#fff"
  },
  cardSubtitle: {
    fontSize: 14,
    color: "#6b7280",
    marginBottom: 8,
    paddingHorizontal: 16,
    textAlign: "center"
  },
  cardSummary: {
    fontSize: 12,
    color: "#374151",
  },
  logoutBtn: {
    marginTop: 32,
    marginBottom: 24,
    backgroundColor: "#2563eb",
    paddingVertical: 14,
    paddingHorizontal: 32,
    borderRadius: 12,
  },
  logoutText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 16,
    textAlign: "center",
  },
});
