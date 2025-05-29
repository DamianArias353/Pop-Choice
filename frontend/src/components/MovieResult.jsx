import { buttonClass, containerClass } from "../utils/styles";

export default function MovieResult({ match, onReset }) {
    if (!match) return null;
  
    // Split the content into title and description
    const [title, ...descriptionParts] = match.content.split('|').map(part => part.trim());
    const description = descriptionParts.join(' | ');

    return (
      <div className={`${containerClass.card} text-center max-w-2xl`}>
        <h2 className="text-white text-2xl sm:text-3xl md:text-4xl font-heading mb-4">
          {title}
        </h2>
        
        <div className="text-slate-light text-lg mb-6 space-y-2">
          {description && (
            <p className="text-slate-light/90">
              {description}
            </p>
          )}
          <p className="text-brand-green font-medium">
            Match score: {(match.similarity * 100).toFixed(1)}%
          </p>
        </div>

        <button
          onClick={onReset}
          className={buttonClass.primary}
        >
          Try Another Movie
        </button>
      </div>
    );
  }