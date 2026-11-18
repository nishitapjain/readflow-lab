import { useEffect, useState } from "react";
import { getBooks, getStreak, getPrediction, getUser, getRecentLogs } from "../api/client";
import BookList from "./BookList";
import Heatmap from "./Heatmap";
import ProgressBar from "./ProgressBar";

export default function Dashboard({ onViewBooks }) {
  const [books, setBooks] = useState([]);
  const [streak, setStreak] = useState(null);
  const [user, setUser] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [recentLogs, setRecentLogs] = useState([]);

  useEffect(() => {
    getBooks().then(setBooks);
    getStreak().then(setStreak);
    getUser().then(setUser);
    getRecentLogs(5).then(setRecentLogs);
  }, []);

  useEffect(() => {
    books.filter(b => b.status === "reading").forEach(b => {
      getPrediction(b.id).then(p => setPredictions(prev => ({ ...prev, [b.id]: p })));
    });
  }, [books]);

  const totalPagesRead = books.reduce((sum, b) => sum + (b.pages_completed || 0), 0);
  const currentlyReading = books.filter(b => b.status === "reading").length;
  const todayStr = new Date().toISOString().slice(0, 10);
  const todayPages = recentLogs.filter(l => l.log_date === todayStr).reduce((s, l) => s + l.pages_read, 0);
  const dailyGoal = user?.daily_goal_pages || 10;
  const goalPct = Math.min(100, Math.round((todayPages / dailyGoal) * 100));

  return (
    <div className="page">
      <header className="page-header">
        <h1>Dashboard</h1>
        <p className="page-sub">Your reading, at a glance.</p>
      </header>

      <section className="stat-row">
        <div className="stat-card"><span className="stat-label">Currently Reading</span><span className="stat-value">{currentlyReading}</span></div>
        <div className="stat-card"><span className="stat-label">Total Pages Read</span><span className="stat-value">{totalPagesRead}</span></div>
        <div className="stat-card"><span className="stat-label">Current Streak</span><span className="stat-value">{streak ? `${streak.current_streak}d` : "–"}</span></div>
        <div className="stat-card"><span className="stat-label">Longest Streak</span><span className="stat-value">{streak ? `${streak.longest_streak}d` : "–"}</span></div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>My Books</h2>
          <button type="button" className="link-btn" onClick={onViewBooks}>View All</button>
        </div>
        <BookList limit={3} showToggle={false} />
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <h2>Daily Goal</h2>
          <p>{todayPages} / {dailyGoal} pages today</p>
          <ProgressBar value={goalPct} />
        </div>
        <div className="panel">
          <h2>Pace Prediction</h2>
          {books.filter(b => b.status === "reading").map(b => {
            const p = predictions[b.id];
            return (
              <div key={b.id} className="prediction-row">
                <span className="prediction-title">{b.title}</span>
                <span className="prediction-value">
                  {!p ? "…" : p.message ? p.message : `${p.days_left}d left · finishes ${p.finish_date}`}
                </span>
              </div>
            );
          })}
        </div>
      </section>

      <section className="panel">
        <h2>Recent Reading Logs</h2>
        <ul className="recent-logs">
          {recentLogs.map(l => (
            <li key={l.id}><span>{l.book_title}</span><span>{l.log_date}</span><span>{l.pages_read}p</span></li>
          ))}
        </ul>
      </section>

      <section className="panel">
        <Heatmap compact />
      </section>
    </div>
  );
}