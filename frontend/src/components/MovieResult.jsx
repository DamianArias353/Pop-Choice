import { buttonClass, containerClass } from "../utils/styles";

export default function MovieResult({ match, onReset }) {
    if (!match) return null;
  
    return (
      <div className={`${containerClass.card} text-center`}>
        <h2 className="text-white text-2xl sm:text-3xl md:text-4xl font-heading mb-4">
          {match.content}
        </h2>
        <p className="text-slate-light text-lg mb-8">
          Similarity score: {(match.similarity * 100).toFixed(1)}%
        </p>
        <button
          onClick={onReset}
          className={buttonClass.primary}
        >
          Go Again
        </button>
      </div>
    );
  }