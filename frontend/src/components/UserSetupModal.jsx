import { useState } from "react";
import { createUser } from "../api/client";

export default function UserSetupModal({ onComplete }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [goal, setGoal] = useState(10);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) { setError("Please enter your name."); return; }
    const user = await createUser({ name: name.trim(), email: email.trim(), daily_goal_pages: Number(goal) || 10 });
    onComplete(user);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <h2>Welcome to ReadFlow</h2>
        <p className="modal-sub">Let's set up your reading profile.</p>
        {error && <p className="form-error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Name
            <input value={name} onChange={e => setName(e.target.value)} required />
          </label>
          <label>Email
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </label>
          <label>Daily page goal
            <input type="number" min="1" value={goal} onChange={e => setGoal(e.target.value)} />
          </label>
          <button type="submit">Get Started</button>
        </form>
      </div>
    </div>
  );
}