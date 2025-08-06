import * as React from 'react';
import { View, Image, StyleSheet, FlatList, Dimensions, TouchableOpacity, Text, ActivityIndicator, TextInput } from 'react-native';
import { useRouter } from 'expo-router';
import { useFocusEffect } from 'expo-router';
import { Audio } from 'expo-av';
import { useBooks } from '../hooks/useBooks';
import SoundManager from "./utils/soundManager";

const { width } = Dimensions.get("window");

export default function LibraryScreen() {
  const router = useRouter();
  const { books, loading } = useBooks() as { books: any[], loading: boolean };

  const [searchQuery, setSearchQuery] = React.useState("");

  useFocusEffect(
  React.useCallback(() => {
    SoundManager.stopAll(); // force stop svih zvukova kad udjes u Library
  }, [])
);

  // Filter books
  const filteredBooks = books.filter((book) =>
    book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
    {/* Search Input */}
    <View style={styles.searchInputHolder}>
      <Text style={styles.searchText}>Find a Book to Dive Into</Text>
      <TextInput
        style={styles.searchInput}
        placeholder=""
        placeholderTextColor="#888"
        value={searchQuery}
        onChangeText={setSearchQuery}
        autoCorrect={false}
        autoCapitalize="none"
      />
    </View>
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator style={{ marginTop: 24 }} size="large" color="#2563eb" />
      ) : (
        <FlatList
          contentContainerStyle={styles.row}
          data={filteredBooks}
          keyExtractor={(item) => item.id.toString()}
          numColumns={3}
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
                <Text style={styles.cardSubtitle}>{item.author}</Text>
                <Text style={styles.cardTitle}>{item.title}</Text>
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
    </>
  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    alignSelf: "center",
    width: "100%",
    maxWidth: 1200,
  },
  searchInputHolder: {
    paddingHorizontal: 16,
    marginTop: 20
  },
  searchInput: {
    width: "100%",
    maxWidth: 400,
    height: 50,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 30,
    alignSelf: "center",
    backgroundColor: "#fff",
    color: "#0A0414",
    fontFamily: "Montserrat_700Bold",
  },
  searchText: {
    fontSize: width * 0.05,
    fontWeight: "bold",
    marginBottom: 4,
    color: "#fff",
    fontFamily: "Montserrat_700Bold",
  },
  row: {
    paddingHorizontal: 8,
    paddingBottom: 16,
    marginBottom: 30,
  },
  cardWrapper: {
    flex: 1,
    padding: 5,
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
    aspectRatio: 2 / 3,
    borderRadius: 4,
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: width * 0.025,
    fontWeight: "bold",
    marginBottom: 4,
    color: "#fff",
    fontFamily: "Montserrat_500Medium",
  },
  cardSubtitle: {
    fontSize: width * 0.024,
    color: "#B3B3B3",
    marginBottom: 0,
    textAlign: "left",
    fontFamily: "Montserrat_300Light",

  },
});
