import { Link } from "react-router-dom";
import { useState } from "react";

// Map category name → CSS class suffix
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
    const diff = Math.floor((now - d) / 60000); // minutes

    if (diff < 1) return "Just now";
    if (diff < 60) return `${diff}m ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`;
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  } catch {
    return dateStr;
  }
}

export default function NewsCard({ article }) {
  const [imgError, setImgError] = useState(false);

  const categoryClass = CATEGORY_CLASS[article.category] || "general";
  const imageSrc = imgError ? PLACEHOLDER : (article.image || PLACEHOLDER);
  const timeLabel = formatTime(article.published_at || article.created_date);

  return (
    <Link
      to={`/news/${article.id}`}
      className="news-card"
      id={`news-card-${article.id}`}
      aria-label={`Read article: ${article.title}`}
    >
      {/* Image */}
      <div className="card-image-wrap">
        <img
          src={imageSrc}
          alt={article.title}
          className="card-image"
          onError={() => setImgError(true)}
          loading="lazy"
        />
        <div className="card-image-overlay" aria-hidden="true" />
      </div>

      {/* Body */}
      <div className="card-body">
        <div className="card-meta">
          <span className={`badge badge-${categoryClass}`}>
            {article.category || "General"}
          </span>
          <span className="card-time">{timeLabel}</span>
        </div>

        <h3 className="card-title">{article.title}</h3>

        {article.description && (
          <p className="card-desc">{article.description}</p>
        )}

        {article.source && (
          <span className="card-source">
            {typeof article.source === "object"
              ? article.source.name
              : article.source}
          </span>
        )}

        <span className="card-read-more">
          Read Article →
        </span>
      </div>
    </Link>
  );
}