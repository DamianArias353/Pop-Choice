// src/api/recommend.js
const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

export async function getRecommendation(answers) {
  const res = await fetch(`${BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers),
  });
  if (!res.ok) throw new Error("Backend error");
  return res.json();   // { id, content, similarity }
}