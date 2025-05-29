import { useState } from "react";
import MovieForm from "./components/MovieForm";
import MovieResult from "./components/MovieResult";
import popcorn from "./assets/popcorn.png";
import { containerClass } from "./utils/styles";

export default function App() {
  const [match, setMatch] = useState(null); // null: muestra formulario

  const handleReset = () => setMatch(null);

  return (
    <div className={containerClass.page}>
      {/* LOGO + título */}
      <header className="flex flex-col items-center gap-3 sm:gap-4">
        <img 
          src={popcorn} 
          alt="PopChoice logo" 
          className="w-20 sm:w-24 md:w-28 drop-shadow-popcorn transition-all duration-300 hover:scale-105" 
        />
        <h1 className="text-white font-heading font-bold text-3xl sm:text-4xl md:text-5xl">
          PopChoice
        </h1>
      </header>

      {/* Contenido principal */}
      <main className="w-full max-w-2xl mx-auto px-4">
        {match ? (
          <MovieResult match={match} onReset={handleReset} />
        ) : (
          <MovieForm onResult={setMatch} />
        )}
      </main>
    </div>
  );
}
