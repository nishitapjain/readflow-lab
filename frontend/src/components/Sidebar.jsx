import { useEffect, useState } from "react";
import { getUser } from "../api/client";

const NAV_ITEMS = [
  { key: "dashboard", label: "Dashboard" },
  { key: "books", label: "Books" },
  { key: "log", label: "Log Reading" },
  { key: "streak", label: "Streak" },
  { key: "activity", label: "Activity" }
];

export default function Sidebar({ activeView, onNavigate }) {
  const [user, setUser] = useState(null);

  useEffect(() => { getUser().then(setUser); }, [activeView]);

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">ReadFlow</div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map(item => (
          <button
            key={item.key}
            type="button"
            className={"nav-item" + (activeView === item.key ? " active" : "")}
            onClick={() => onNavigate(item.key)}
          >
            {item.label}
          </button>
        ))}
      </nav>
      {user?.name && (
        <div className="sidebar-footer">
          <div className="sidebar-footer-name">{user.name}</div>
          <div className="sidebar-footer-sub">Goal: {user.daily_goal_pages} pages/day</div>
        </div>
      )}
    </aside>
  );
}