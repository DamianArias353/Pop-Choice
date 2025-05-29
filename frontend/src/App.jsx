import { useState } from "react";
import MovieForm from "./components/MovieForm";
import MovieResult from "./components/MovieResult";
import popcorn from "./assets/popcorn.png";

export default function App() {
  const [match, setMatch] = useState(null);

  return (
    <div className="container">
      <img src={popcorn} alt="PopChoice" className="logo" />
      <h1>PopChoice</h1>

      {match ? (
        <MovieResult match={match} onReset={() => setMatch(null)} />
      ) : (
        <MovieForm onResult={setMatch} />
      )}
    </div>
  );
}