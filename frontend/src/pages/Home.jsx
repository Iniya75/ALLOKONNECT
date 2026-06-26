import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { getNews } from "../api/newsApi";
import NewsCard from "../components/NewsCard";

const CATEGORY_CLASS = {
  "Gadgets": "gadgets",
  "AI Hub": "ai-hub",
  "Finance": "finance",
  "World News": "world-news",
  "Open Source": "open-source",
  "Space Station": "space-station",
  "Features": "features",
};

const PLACEHOLDER = "/images/placeholder.jpg";

function formatTime(dateStr) {
  if (!dateStr) return "";
  try {
    const d = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - d) / 60000);
    if (diff < 1) return "Just now";
    if (diff < 60) return `${diff}m ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`;
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  } catch { return dateStr; }
}

/* ── Skeleton card ─────────────────────────────────────────────────────── */
function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-img" />
      <div className="skeleton-body">
        <div className="skeleton skeleton-badge" />
        <div className="skeleton skeleton-title" />
        <div className="skeleton skeleton-title-2" />
        <div className="skeleton skeleton-text" />
        <div className="skeleton skeleton-text-2" />
      </div>
    </div>
  );
}

/* ── Hero card ─────────────────────────────────────────────────────────── */
function HeroCard({ article }) {
  const [imgError, setImgError] = useState(false);
  const imageSrc = imgError ? PLACEHOLDER : (article.image || PLACEHOLDER);
  const catClass = CATEGORY_CLASS[article.category] || "general";

  return (
    <Link
      to={`/news/${article.id}`}
      className="hero-card"
      id={`hero-card-${article.id}`}
      aria-label={`Featured: ${article.title}`}
    >
      <div className="hero-image-wrap">
        <img
          src={imageSrc}
          alt={article.title}
          className="hero-image"
          onError={() => setImgError(true)}
        />
        <div className="hero-gradient" aria-hidden="true" />
      </div>

      <div className="hero-content">
        <div className="hero-meta">
          <span className={`badge badge-${catClass}`}>
            {article.category || "General"}
          </span>
          <span className="hero-time">
            {formatTime(article.published_at || article.created_date)}
          </span>
        </div>
        <h2 className="hero-title">{article.title}</h2>
        {article.description && (
          <p className="hero-desc">{article.description}</p>
        )}
      </div>
    </Link>
  );
}

/* ── Home page ─────────────────────────────────────────────────────────── */
export default function Home() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [searchParams] = useSearchParams();

  const activeCategory = searchParams.get("category");

  useEffect(() => {
    let mounted = true;

    async function fetchNews() {
      try {
        const data = await getNews();
        if (mounted) {
          setNews(data);
          setLoading(false);
        }
      } catch {
        if (mounted) {
          setError(true);
          setLoading(false);
        }
      }
    }

    fetchNews();
    return () => { mounted = false; };
  }, []);

  /* ── Loading state ─────────────────────────────────────────────────── */
  if (loading) {
    return (
      <main className="home" aria-label="Loading news">
        <div className="hero-wrapper">
          <div className="skeleton-card" style={{ borderRadius: "28px" }}>
            <div className="skeleton skeleton-img"
              style={{ aspectRatio: "16/7" }} />
          </div>
        </div>
        <div className="news-grid">
          {Array.from({ length: 6 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </main>
    );
  }

  /* ── Error state ───────────────────────────────────────────────────── */
  if (error) {
    return (
      <main className="home">
        <div className="empty-state">
          <div className="empty-state-icon">⚠️</div>
          <h3>Could not load news</h3>
          <p>Make sure the backend is running at localhost:8000</p>
        </div>
      </main>
    );
  }

  // Filter by category if selected
  const displayedNews = activeCategory
    ? news.filter(article => article.category === activeCategory)
    : news;

  if (!displayedNews || displayedNews.length === 0) {
    return (
      <main className="home">
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <h3>No articles found</h3>
          <p>
            {activeCategory
              ? `There are no articles in the "${activeCategory}" category yet.`
              : "The scheduler will publish the first article at 06:00, 10:00, 14:00 or 18:00 IST."}
          </p>
          {activeCategory && (
            <Link to="/" style={{ color: "var(--accent)", marginTop: "16px", display: "inline-block" }}>
              View all news
            </Link>
          )}
        </div>
      </main>
    );
  }

  const [featured, ...rest] = displayedNews;

  return (
    <main className="home" aria-label="News feed">

      {/* Featured hero */}
      {featured && (
        <section className="hero-wrapper" aria-label="Featured article">
          <div className="section-heading">
            <h2>Featured</h2>
            <div className="section-divider" />
          </div>
          <HeroCard article={featured} />
        </section>
      )}

      {/* Rest of articles */}
      {rest.length > 0 && (
        <section className="grid-section" aria-label="Latest articles">
          <div className="section-heading">
            <h2>Latest</h2>
            <div className="section-divider" />
          </div>
          <div className="news-grid">
            {rest.map((article) => (
              <NewsCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

    </main>
  );
}