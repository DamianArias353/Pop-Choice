import { useState } from "react";
import { getRecommendation } from "../api/recommend";

export default function MovieForm({ onResult }) {
  const [form, setForm] = useState({ q1: "", q2: "", q3: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await getRecommendation(form);
      onResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="stack" onSubmit={handleSubmit}>
      <label>
        What’s your favorite movie and why?
        <textarea name="q1" value={form.q1} onChange={handleChange} required />
      </label>

      <label>
        Are you in the mood for something new or a classic?
        <input name="q2" value={form.q2} onChange={handleChange} required />
      </label>

      <label>
        Do you wanna have fun or do you want something serious?
        <input name="q3" value={form.q3} onChange={handleChange} required />
      </label>

      {error && <p className="error">{error}</p>}
      <button disabled={loading}>{loading ? "Thinking..." : "Let’s Go"}</button>
    </form>
  );
}