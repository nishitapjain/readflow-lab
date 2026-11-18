// Mock data layer only. No network requests, no backend, no API keys.
// Function names/shapes mirror the backend's documented contract so this
// file alone can later be swapped for real fetch() calls.
import { mockUser, mockBooks, mockLogs, mockStreak, mockHeatmap, mockBadges } from "../mockData";

function delay(value) {
  return new Promise(resolve => setTimeout(() => resolve(value), 100));
}

export function createUser({ name, email, daily_goal_pages }) {
  Object.assign(mockUser, { name, email, daily_goal_pages });
  return delay({ ...mockUser });
}

export function getUser() {
  return delay(mockUser.name ? { ...mockUser } : null);
}

export function getBooks() {
  return delay([...mockBooks]);
}

export function addBook({ title, author, total_pages }) {
  const newBook = { id: Date.now(), title, author, total_pages, pages_completed: 0, status: "reading" };
  mockBooks.push(newBook);
  return delay(newBook);
}

export function updateBookStatus(bookId, status) {
  const book = mockBooks.find(b => b.id === bookId);
  if (book) book.status = status;
  return delay(book);
}

export function logReading({ book_id, pages_read, log_date }) {
  const entry = { id: Date.now(), book_id, pages_read, log_date };
  mockLogs.push(entry);
  const book = mockBooks.find(b => b.id === book_id);
  if (book) {
    book.pages_completed = Math.min(book.total_pages, (book.pages_completed || 0) + pages_read);
    if (book.pages_completed >= book.total_pages) book.status = "finished";
  }
  return delay(entry);
}

export function getBookLogs(bookId) {
  return delay(mockLogs.filter(l => l.book_id === bookId));
}

export function getRecentLogs(limit = 5) {
  return delay(
    [...mockLogs]
      .sort((a, b) => (b.log_date || "").localeCompare(a.log_date || ""))
      .slice(0, limit)
      .map(l => ({ ...l, book_title: mockBooks.find(b => b.id === l.book_id)?.title || "Unknown" }))
  );
}

// Exact formula from the backend README: last 7 calendar days (zero-filled),
// requires logs on >=3 distinct dates, ceil(remaining / avgDaily).
export function getPrediction(bookId) {
  const book = mockBooks.find(b => b.id === bookId);
  if (!book) return delay({ message: "Not enough data" });

  const logsForBook = mockLogs.filter(l => l.book_id === bookId);
  const distinctDays = new Set(logsForBook.map(l => l.log_date)).size;

  const today = new Date();
  let last7Sum = 0;
  for (let i = 0; i < 7; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const key = d.toISOString().slice(0, 10);
    last7Sum += logsForBook.filter(l => l.log_date === key).reduce((s, l) => s + l.pages_read, 0);
  }
  const avgDaily = last7Sum / 7;

  if (distinctDays < 3 || avgDaily === 0) {
    return delay({ message: "Not enough data" });
  }

  const totalLogged = logsForBook.reduce((s, l) => s + l.pages_read, 0);
  const remaining = Math.max(0, book.total_pages - totalLogged);
  const daysLeft = Math.ceil(remaining / avgDaily);
  const finishDate = new Date(today);
  finishDate.setDate(finishDate.getDate() + daysLeft);

  return delay({ days_left: daysLeft, finish_date: finishDate.toISOString().slice(0, 10) });
}

export function getStreak() {
  return delay({ ...mockStreak });
}

export function getHeatmap(days = 90) {
  return delay(mockHeatmap.slice(-days));
}

export function getBadges() {
  return delay([...mockBadges]);
}