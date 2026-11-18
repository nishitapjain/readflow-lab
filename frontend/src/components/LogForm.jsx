import { useEffect, useState } from "react";
import { getBooks, logReading } from "../api/client";

export default function LogForm({ onLogged }) {
  const [books, setBooks] = useState([]);
  const [bookId, setBookId] = useState("");
  const [pages, setPages] = useState("");
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [message, setMessage] = useState(null);

  useEffect(() => { getBooks().then(setBooks); }, []);

  const selectedBook = books.find(b => b.id === Number(bookId));
  const remaining = selectedBook ? selectedBook.total_pages - (selectedBook.pages_completed || 0) : null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);

    if (!bookId) { setMessage({ type: "error", text: "Please select a book." }); return; }

    const pagesNum = Number(pages);
    if (!pages || pagesNum <= 0) { setMessage({ type: "error", text: "Enter a positive number of pages." }); return; }

    if (remaining !== null && pagesNum > remaining) {
      setMessage({ type: "error", text: `This book only has ${remaining} page(s) left.` });
      return;
    }

    await logReading({ book_id: Number(bookId), pages_read: pagesNum, log_date: date });
    setPages("");
    setMessage({ type: "success", text: "Reading logged!" });
    onLogged && onLogged();
  };

  return (
    <form onSubmit={handleSubmit} className="log-form">
      <h2>Log Reading</h2>
      {message && <p className={`form-${message.type}`}>{message.text}</p>}
      <label>Book
        <select value={bookId} onChange={e => setBookId(e.target.value)} required>
          <option value="">Select a book</option>
          {books.map(b => <option key={b.id} value={b.id}>{b.title}</option>)}
        </select>
      </label>
      {selectedBook && <p className="field-hint">{remaining} page(s) remaining</p>}
      <label>Pages read
        <input type="number" value={pages} onChange={e => setPages(e.target.value)} required min="1" />
      </label>
      <label>Date
        <input type="date" value={date} onChange={e => setDate(e.target.value)} />
      </label>
      <button type="submit">Log Reading</button>
    </form>
  );
}