import { Link, useSearchParams } from "react-router-dom";

const CATEGORIES = [
  "All", "Gadgets", "AI Hub", "Finance", "World News",
  "Open Source", "Space Station", "Features"
];

export default function Navbar() {
  const [searchParams] = useSearchParams();
  const activeCat = searchParams.get("category") || "All";

  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar-inner">

        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <div className="navbar-logo-icon" aria-hidden="true">⚡</div>
          <span className="navbar-logo-text">NewsFeed AI</span>
        </Link>

        {/* Category strip */}
        <div className="navbar-categories" role="list">
          {CATEGORIES.map((cat) => {
            const isActive = activeCat === cat;
            const toPath = cat === "All" ? "/" : `/?category=${encodeURIComponent(cat)}`;
            
            return (
              <Link
                key={cat}
                to={toPath}
                className="navbar-cat-btn"
                role="listitem"
                aria-label={`Filter by ${cat}`}
                style={isActive ? { 
                  background: "var(--accent)", 
                  color: "#fff", 
                  borderColor: "var(--accent)",
                  boxShadow: "0 4px 12px rgba(108, 99, 255, 0.3)"
                } : {
                  textDecoration: "none"
                }}
              >
                {cat}
              </Link>
            );
          })}
        </div>

        {/* Live indicator */}
        <div className="navbar-live" aria-label="Live feed">
          <span className="navbar-live-dot" aria-hidden="true" />
          LIVE
        </div>

      </div>
    </nav>
  );
}