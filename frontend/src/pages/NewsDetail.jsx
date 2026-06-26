import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getNewsById } from "../api/newsApi";

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

function formatDate(dateStr) {
  if (!dateStr) return "";
  try {
    return new Date(dateStr).toLocaleDateString("en-US", {
      year: "numeric", month: "long", day: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  } catch { return dateStr; }
}

function DetailSkeleton() {
  return (
    <div className="detail-skeleton">
      <div className="skeleton" style={{ height: 400, borderRadius: 20 }} />
      <div className="skeleton skeleton-badge" />
      <div className="skeleton skeleton-title" style={{ height: 36, width: "80%" }} />
      <div className="skeleton skeleton-text" style={{ marginTop: 16 }} />
      {Array.from({ length: 10 }).map((_, i) => (
        <div key={i} className="skeleton skeleton-text"
          style={{ width: i % 3 === 0 ? "75%" : "100%" }} />
      ))}
    </div>
  );
}

export default function NewsDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imgError, setImgError] = useState(false);

  useEffect(() => {
    let mounted = true;

    async function fetchArticle() {
      setLoading(true);
      const data = await getNewsById(id);
      if (mounted) {
        setArticle(data);
        setLoading(false);
      }
    }

    fetchArticle();
    window.scrollTo({ top: 0, behavior: "smooth" });

    return () => { mounted = false; };
  }, [id]);

  if (loading) return <DetailSkeleton />;

  if (!article) {
    return (
      <div className="error-page">
        <div style={{ fontSize: 56 }}>🔍</div>
        <h2>Article Not Found</h2>
        <p>This article may have been removed or the ID is incorrect.</p>
        <button className="back-btn" onClick={() => navigate("/")}>
          ← Back to Home
        </button>
      </div>
    );
  }

  const catClass = CATEGORY_CLASS[article.category] || "general";
  const imageSrc = imgError ? PLACEHOLDER : (article.image || PLACEHOLDER);
  const source = typeof article.source === "object"
    ? article.source?.name : article.source;

  return (
    <article className="detail-page" aria-label={article.title}>

      {/* ── Hero image ───────────────────────────────────────────────── */}
      <div className="detail-hero">
        <img
          src={imageSrc}
          alt={article.title}
          className="detail-hero-img"
          onError={() => setImgError(true)}
        />
        <div className="detail-hero-overlay" aria-hidden="true" />
        <div className="detail-hero-meta">
          <div className="detail-hero-badge">
            <span className={`badge badge-${catClass}`}>
              {article.category || "General"}
            </span>
          </div>
          <h1 className="detail-hero-title">{article.title}</h1>
        </div>
      </div>

      {/* ── Article body ─────────────────────────────────────────────── */}
      <div className="detail-body">

        {/* Back button */}
        <button
          className="back-btn"
          onClick={() => navigate(-1)}
          id="back-btn"
          aria-label="Go back to news feed"
        >
          ← Back
        </button>

        {/* Meta info bar */}
        <div className="detail-info-bar" role="contentinfo">
          {article.published_at && (
            <div className="detail-info-item">
              <span className="detail-info-label">Published:</span>
              {formatDate(article.published_at)}
            </div>
          )}
          {article.created_date && (
            <div className="detail-info-item">
              <span className="detail-info-label">Added:</span>
              {article.created_date} {article.created_time || ""}
            </div>
          )}
          {source && (
            <div className="detail-info-item">
              <span className="detail-info-label">Source:</span>
              {source}
            </div>
          )}
        </div>

        {/* AI Summary (~300 words) */}
        {article.summary && (
          <section className="detail-section" aria-label="AI summary">
            <div className="detail-section-title">AI Summary</div>
            <p className="detail-summary">{article.summary}</p>
          </section>
        )}

        {/* Detailed description / lead paragraph */}
        {article.description && article.description !== article.summary && (
          <section className="detail-section" aria-label="Article description">
            <div className="detail-section-title">Quick Take</div>
            <div className="detail-description">{article.description}</div>
          </section>
        )}

        {/* External Read More Link */}
        {article.url && (
          <div style={{ marginTop: "40px", textAlign: "center" }}>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="read-more-link"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "12px 24px",
                background: "var(--accent)",
                color: "#fff",
                borderRadius: "30px",
                textDecoration: "none",
                fontWeight: "600",
                fontSize: "1.05rem",
                transition: "all 0.2s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-2px)";
                e.currentTarget.style.boxShadow = "0 8px 16px rgba(139, 92, 246, 0.4)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "none";
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              Read Original Article <span style={{ fontSize: "1.2rem" }}>↗</span>
            </a>
          </div>
        )}

      </div>
    </article>
  );
}
