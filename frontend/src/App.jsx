import { useEffect, useMemo, useState } from 'react';

const SURPRISE_MOVIES = [
  'Avatar',
  "Pirates of the Caribbean: At World's End",
  'Spectre',
  'The Dark Knight',
  'Inception',
  'Interstellar',
  'The Matrix',
  'The Avengers',
];

const buildGenreChips = (genres) => {
  return genres
    .split(' ')
    .filter(Boolean)
    .slice(0, 5);
};

const App = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState('Search anything cinematic.');
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [mode, setMode] = useState('Ultra Premium');

  const heroText = useMemo(() => {
    if (!query) return 'Fuzzily match your title, vibe, or cast in a luxury glass interface.';
    if (query.length < 5) return 'Type more to unlock deeper movie connections.';
    return 'Tap enter, select a suggestion, or ask for a surprise cinematic shot.';
  }, [query]);

  useEffect(() => {
    if (!query) {
      setSuggestions([]);
      return;
    }

    const timeout = setTimeout(() => {
      fetchSuggestions(query);
    }, 160);

    return () => clearTimeout(timeout);
  }, [query]);

  const fetchSuggestions = async (nextQuery) => {
    try {
      const response = await fetch(`/api/suggest?query=${encodeURIComponent(nextQuery)}`);
      const data = await response.json();
      setSuggestions(Array.isArray(data.results) ? data.results : []);
      setActiveIndex(-1);
    } catch (error) {
      console.error(error);
      setSuggestions([]);
    }
  };

  const fetchResults = async (searchTerm) => {
    setLoading(true);
    setStatus('Generating premium recommendations...');
    setResults([]);
    setSuggestions([]);

    try {
      const response = await fetch(`/api/recommend?movie=${encodeURIComponent(searchTerm)}`);
      const data = await response.json();

      if (data.message) {
        setStatus(data.message);
        setResults([]);
      } else if (Array.isArray(data.recommendations) && data.recommendations.length) {
        setResults(data.recommendations);
        setStatus(`Showing ${data.recommendations.length} premium picks for “${searchTerm}”.`);
      } else {
        setStatus('No premium recommendations found. Try another title.');
      }
    } catch (error) {
      console.error(error);
      setStatus('Unable to fetch recommendations. Please check that the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const chooseSuggestion = (title) => {
    setQuery(title);
    setSuggestions([]);
    fetchResults(title);
  };

  const handleKeyDown = (event) => {
    if (!suggestions.length) return;

    if (event.key === 'ArrowDown') {
      setActiveIndex((index) => Math.min(index + 1, suggestions.length - 1));
    }

    if (event.key === 'ArrowUp') {
      setActiveIndex((index) => Math.max(index - 1, 0));
    }

    if (event.key === 'Enter') {
      if (activeIndex >= 0 && activeIndex < suggestions.length) {
        chooseSuggestion(suggestions[activeIndex]);
      } else {
        fetchResults(query.trim());
      }
    }

    if (event.key === 'Escape') {
      setSuggestions([]);
      setActiveIndex(-1);
    }
  };

  const surpriseMe = () => {
    const random = SURPRISE_MOVIES[Math.floor(Math.random() * SURPRISE_MOVIES.length)];
    setQuery(random);
    fetchResults(random);
  };

  return (
    <div className="app-shell">
      <header className="header">
        <div className="title-group">
          <h1>Movie Recommender</h1>
          <span className="tag">{mode}</span>
        </div>
        <p className="subtitle">{heroText}</p>

        <div className="control-panel">
          <div className="search-group">
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Search movie title or mood"
              autoComplete="off"
            />
            <button disabled={!query.trim()} onClick={() => fetchResults(query.trim())}>
              Launch
            </button>

            {suggestions.length > 0 && (
              <ul className="suggestions">
                {suggestions.map((title, index) => (
                  <li
                    key={title}
                    className={index === activeIndex ? 'active' : ''}
                    onMouseDown={() => chooseSuggestion(title)}
                  >
                    {title}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="action-group">
            <button onClick={surpriseMe}>Surprise Me</button>
            <button onClick={() => setMode((prev) => (prev === 'Ultra Premium' ? 'Zen Velvet' : 'Ultra Premium'))}>
              {mode === 'Ultra Premium' ? 'Zen Mode' : 'Ultra Premium'}
            </button>
          </div>
        </div>
      </header>

      <main className="result-grid">
        {loading ? (
          <div className="movie-card">
            <h2>Spinning the recommendation engine...</h2>
            <p className="tagline">Premium neural compute in progress.</p>
          </div>
        ) : results.length ? (
          results.map((item) => (
            <article className="movie-card" key={`${item.title}-${item.release_date}`}>
              <h2>{item.title}</h2>
              <p className="tagline">{item.tagline || 'No tagline available.'}</p>
              <div className="metadata">
                {buildGenreChips(item.genres).map((genre) => (
                  <span key={`${item.title}-${genre}`}>{genre}</span>
                ))}
              </div>
              <div className="detail">
                <p>
                  <strong>Release:</strong> {item.release_date || 'Unknown'}
                </p>
                <p>
                  <strong>Rating:</strong> {item.vote_average || 'N/A'}
                </p>
                <p>
                  <strong>Director:</strong> {item.director || 'Unknown'}
                </p>
                <p>
                  <strong>Cast:</strong> {item.cast || 'N/A'}
                </p>
                <p>{item.overview || 'No overview available.'}</p>
              </div>
            </article>
          ))
        ) : (
          <div className="empty-state">
            <p>{status}</p>
            <p className="data-note">Try typing something like “Avatar”, “Inception”, or “Pirates”.</p>
          </div>
        )}
      </main>

      <footer className="footer">Premium UI built with React & FastAPI — hard mode activated.</footer>
    </div>
  );
};

export default App;
