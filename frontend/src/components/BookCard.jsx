import ProgressBar from "./ProgressBar";

export default function BookCard({ book, onToggleStatus }) {
  const pct = book.total_pages ? Math.round((book.pages_completed / book.total_pages) * 100) : 0;

  return (
    <div className="book-card">
      <div className="book-card-top">
        <div>
          <h3 className="book-card-title">{book.title}</h3>
          <p className="book-card-author">by {book.author}</p>
        </div>
        <span className={`status-pill ${book.status}`}>{book.status}</span>
      </div>
      <p className="book-card-pages">{book.pages_completed || 0} / {book.total_pages} pages</p>
      <ProgressBar value={pct} />
      <div className="book-card-footer">
        <span className="progress-pct">{pct}%</span>
        {onToggleStatus && (
          <button type="button" className="link-btn" onClick={() => onToggleStatus(book)}>
            {book.status === "finished" ? "Mark as reading" : "Mark as finished"}
          </button>
        )}
      </div>
    </div>
  );
}