const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

const API_BASE = `${API_BASE_URL}/api`;
const BOOKS_URL = `${API_BASE}/books`;
const SOUNDSCAPE_URL = `${API_BASE_URL}/soundscape`;

export const fetchBooks = async () => {
  const res = await fetch(BOOKS_URL);
  if (!res.ok) throw new Error("Failed to fetch books");
  return res.json();
};

export const fetchBook = async (bookId: string | number) => {
  const res = await fetch(`${BOOKS_URL}/${bookId}`);
  if (!res.ok) throw new Error("Failed to fetch book");
  return res.json();
};

export const fetchSoundscape = async (
  bookId: string | number,
  chapterNumber: number,
  pageNumber: number
) => {
  const url = `${SOUNDSCAPE_URL}/book/${bookId}`;
  console.log("🔗 Fetching Soundscape from:", url);

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch soundscape");

  const data = await res.json();

  // Pretty print JSON in Metro logs
  console.log("📄 Soundscape JSON Response:", JSON.stringify(data, null, 2));

  return data as {
    book_id: number;
    book_page_id: number;
    summary: string;
    detected_scenes: string[];
    scene_keyword_counts: Record<string, number>;
    scene_keyword_positions: Record<string, number[]>;
    carpet_tracks: string[];
    triggered_sounds: Array<{ word: string; position: number; file: string }>;
  };
};
