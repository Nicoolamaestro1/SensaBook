import { useEffect, useState } from "react";
import { fetchBook, fetchBooks } from "../api/books";

export const useBooks = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBooks()
      .then(setBooks)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return { books, loading };
}

export const useBook = (bookId: string) => {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBook(bookId)
      .then(setBook)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [bookId]);

  return { book, loading };
};