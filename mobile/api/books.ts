const API_URL = "http://127.0.0.1:8000/api/books";

export const fetchBooks = async () => {
  const res = await fetch(`${API_URL}`);
  if (!res.ok) throw new Error("Failed to fetch books");
  return res.json();
}

export const fetchBook = async (bookId: string) => {
  const res = await fetch(`${API_URL}/${bookId}`);
  if (!res.ok) throw new Error("Failed to fetch book");
  return res.json();
}