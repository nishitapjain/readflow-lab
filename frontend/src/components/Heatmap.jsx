import { useEffect, useState } from "react";
import { getHeatmap } from "../api/client";

export default function Heatmap({ compact = false }) {
  const [data, setData] = useState([]);

  useEffect(() => { getHeatmap(90).then(setData); }, []);

  const intensity = (pages) => {
    if (pages === 0) return "none";
    if (pages < 10) return "low";
    if (pages < 25) return "mid";
    return "high";
  };

  const visible = compact ? data.slice(-35) : data;

  return (
    <div className="heatmap">
      <h2>{compact ? "Recent Activity" : "Last 90 Days"}</h2>
      <div className="heatmap-grid">
        {visible.map(day => (
          <div key={day.date} className={`cell ${intensity(day.pages)}`} title={`${day.date}: ${day.pages} pages`} />
        ))}
      </div>
      <div className="heatmap-legend">
        <span>Less</span>
        <span className="cell none" />
        <span className="cell low" />
        <span className="cell mid" />
        <span className="cell high" />
        <span>More</span>
      </div>
    </div>
  );
}