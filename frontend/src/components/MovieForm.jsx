import { useState } from "react";
import { getRecommendation } from "../api/recommend";
import { buttonClass, inputClass, containerClass } from "../utils/styles";

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
      setError("Algo salió mal, inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={containerClass.form}>
      <div className={containerClass.card}>
        <label className="text-left text-white font-medium">
          What's your favorite movie and why?
          <textarea
            required
            name="q1"
            value={form.q1}
            onChange={handleChange}
            className={`${inputClass.base} ${inputClass.textarea} mt-2`}
            placeholder="Tell us about your favorite movie..."
          />
        </label>

        <label className="text-left text-white font-medium mt-6">
          Are you in the mood for something new or a classic?
          <input
            required
            name="q2"
            value={form.q2}
            onChange={handleChange}
            className={`${inputClass.base} mt-2`}
            placeholder="New or classic?"
          />
        </label>

        <label className="text-left text-white font-medium mt-6">
          Do you wanna have fun or do you want something serious?
          <input
            required
            name="q3"
            value={form.q3}
            onChange={handleChange}
            className={`${inputClass.base} mt-2`}
            placeholder="Fun or serious?"
          />
        </label>

        {error && (
          <p className="text-red-400 text-sm mt-4 animate-shake">
            {error}
          </p>
        )}
      </div>

      <button
        disabled={loading}
        className={buttonClass.primary}
      >
        {loading ? "Thinking…" : "Let's Go"}
      </button>
    </form>
  );
}