function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
}

export const mockUser = {
  id: 1,
  name: "",
  email: "",
  daily_goal_pages: 10
};

export const mockBooks = [
  { id: 1, title: "Atomic Habits", author: "James Clear", total_pages: 320, pages_completed: 110, status: "reading" }
];

export const mockLogs = [
  { id: 1, book_id: 1, pages_read: 20, log_date: daysAgo(6) },
  { id: 2, book_id: 1, pages_read: 25, log_date: daysAgo(5) },
  { id: 3, book_id: 1, pages_read: 0,  log_date: daysAgo(4) },
  { id: 4, book_id: 1, pages_read: 30, log_date: daysAgo(3) },
  { id: 5, book_id: 1, pages_read: 15, log_date: daysAgo(2) },
  { id: 6, book_id: 1, pages_read: 0,  log_date: daysAgo(1) },
  { id: 7, book_id: 1, pages_read: 20, log_date: daysAgo(0) }
];

export const mockStreak = {
  current_streak: 4,
  longest_streak: 11
};

export const mockHeatmap = Array.from({ length: 90 }, (_, i) => ({
  date: daysAgo(89 - i),
  pages: Math.random() > 0.3 ? Math.floor(Math.random() * 40) : 0
}));

export const mockBadges = [
  { badge_code: "week_warrior", label: "Week Warrior", threshold: 7, awarded_on: daysAgo(3) },
  { badge_code: "month_master", label: "Month Master", threshold: 30, awarded_on: null },
  { badge_code: "century_legend", label: "Century Legend", threshold: 100, awarded_on: null }
];