import { useEffect, useState } from "react";
import { getBooks, updateBookStatus } from "../api/client";
import BookCard from "./BookCard";

export default function BookList({ limit, showToggle = true }) {
  const [books, setBooks] = useState([]);

  const load = () => getBooks().then(setBooks);

  useEffect(() => { load(); }, []);

  const handleToggle = async (book) => {
    const newStatus = book.status === "finished" ? "reading" : "finished";
    await updateBookStatus(book.id, newStatus);
    load();
  };

  const visible = limit ? books.slice(0, limit) : books;

  return (
    <div className="book-grid">
      {visible.map(book => (
        <BookCard key={book.id} book={book} onToggleStatus={showToggle ? handleToggle : null} />
      ))}
      {visible.length === 0 && <p className="empty-state">No books yet. Add your first book to get started.</p>}
    </div>
  );
}