import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import BookList from "./components/BookList";
import AddBookForm from "./components/AddBookForm";
import LogForm from "./components/LogForm";
import StreakDisplay from "./components/StreakDisplay";
import Heatmap from "./components/Heatmap";
import UserSetupModal from "./components/UserSetupModal";
import { getUser } from "./api/client";
import "./App.css";

export default function App() {
  const [view, setView] = useState("dashboard");
  const [user, setUser] = useState(null);
  const [checked, setChecked] = useState(false);
  const [booksRefreshKey, setBooksRefreshKey] = useState(0);

  useEffect(() => {
    getUser().then(u => { setUser(u); setChecked(true); });
  }, []);

  const needsSetup = checked && (!user || !user.name);

  return (
    <div className="app-shell">
      <Sidebar activeView={view} onNavigate={setView} />
      <main className="main-area">
        {view === "dashboard" && <Dashboard onViewBooks={() => setView("books")} />}

        {view === "books" && (
          <div className="page">
            <header className="page-header">
              <h1>Books</h1>
              <p className="page-sub">Your personal reading library.</p>
            </header>
            <section className="panel">
              <AddBookForm onAdded={() => setBooksRefreshKey(k => k + 1)} />
            </section>
            <section className="panel">
              <h2>Your Library</h2>
              <BookList key={booksRefreshKey} />
            </section>
          </div>
        )}

        {view === "log" && (
          <div className="page">
            <header className="page-header">
              <h1>Log Reading</h1>
              <p className="page-sub">Record today's reading session.</p>
            </header>
            <section className="panel panel-narrow">
              <LogForm />
            </section>
          </div>
        )}

        {view === "streak" && (
          <div className="page">
            <header className="page-header">
              <h1>Streak</h1>
              <p className="page-sub">Your reading consistency.</p>
            </header>
            <section className="panel panel-narrow">
              <StreakDisplay />
            </section>
          </div>
        )}

        {view === "activity" && (
          <div className="page">
            <header className="page-header">
              <h1>Activity</h1>
              <p className="page-sub">Your 90-day reading history.</p>
            </header>
            <section className="panel">
              <Heatmap />
            </section>
          </div>
        )}
      </main>
      {needsSetup && <UserSetupModal onComplete={(u) => setUser(u)} />}
    </div>
  );
}