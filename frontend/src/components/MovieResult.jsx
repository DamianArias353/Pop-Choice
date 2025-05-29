export default function MovieResult({ match, onReset }) {
    if (!match) return null;
  
    return (
      <div className="result">
        <h2>{match.content}</h2>
        <p>Similarity score: {(match.similarity * 100).toFixed(1)}%</p>
        <button onClick={onReset}>Go Again</button>
      </div>
    );
  }