export default function ProgressBar({ value }) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className="progress-track">
      <div className="progress-fill" style={{ width: `${pct}%` }} />
    </div>
  );
}