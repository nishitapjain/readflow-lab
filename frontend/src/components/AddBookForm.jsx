import { useState } from "react";
import { addBook } from "../api/client";

export default function AddBookForm({ onAdded }) {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [totalPages, setTotalPages] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!title.trim() || !author.trim() || !totalPages || Number(totalPages) <= 0) {
      setError("Please fill in all fields with a valid page count.");
      return;
    }
    await addBook({ title: title.trim(), author: author.trim(), total_pages: Number(totalPages) });
    setTitle(""); setAuthor(""); setTotalPages("");
    onAdded && onAdded();
  };

  return (
    <form className="add-book-form" onSubmit={handleSubmit}>
      <h2>Add a Book</h2>
      {error && <p className="form-error">{error}</p>}
      <label>Title
        <input value={title} onChange={e => setTitle(e.target.value)} required />
      </label>
      <label>Author
        <input value={author} onChange={e => setAuthor(e.target.value)} required />
      </label>
      <label>Total pages
        <input type="number" min="1" value={totalPages} onChange={e => setTotalPages(e.target.value)} required />
      </label>
      <button type="submit">Add Book</button>
    </form>
  );
}