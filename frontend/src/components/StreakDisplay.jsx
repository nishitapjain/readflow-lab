import { useEffect, useState } from "react";
import { getStreak, getBadges } from "../api/client";

export default function StreakDisplay() {
  const [streak, setStreak] = useState(null);
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    getStreak().then(setStreak);
    getBadges().then(setBadges);
  }, []);

  if (!streak) return <p>Loading streak...</p>;

  return (
    <div className="streak-display">
      <h2>Streak</h2>
      <div className="streak-number-large">{streak.current_streak}</div>
      <p>Current streak (days)</p>
      <p className="streak-secondary">Longest streak: <span>{streak.longest_streak} days</span></p>
      <div className="badges">
        {badges.map(b => (
          <span key={b.badge_code} className={`badge ${b.awarded_on ? "earned" : "locked"}`}>
            {b.label}{b.awarded_on ? "" : ` (${b.threshold}d)`}
          </span>
        ))}
      </div>
    </div>
  );
}