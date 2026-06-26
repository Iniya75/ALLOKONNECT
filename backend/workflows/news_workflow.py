"""
News Workflow — Orchestrates the full article generation pipeline.

Pipeline:
  PlannerAgent → SearchAgent → FilterAgent → WriterAgent → PublisherAgent

Logs are printed at every step for visibility.
"""

from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.filter_agent import FilterAgent
from agents.writer_agent import WriterAgent
from agents.publisher_agent import PublisherAgent

import json
from pathlib import Path

planner = PlannerAgent()
search = SearchAgent()
filter_agent = FilterAgent()
writer = WriterAgent()
publisher = PublisherAgent()

NEWS_FILE = Path(__file__).resolve().parent.parent / "output" / "news.json"


def _load_existing_urls() -> set:
    if NEWS_FILE.exists():
        try:
            with open(NEWS_FILE, "r", encoding="utf-8") as f:
                news = json.load(f)
            return {item.get("url", "") for item in news}
        except Exception:
            pass
    return set()


def run_news_workflow() -> dict | None:
    """
    Run the complete news generation pipeline.
    Returns the newly published article dict, or None if nothing was saved.
    """
    print("\n" + "=" * 55)
    print("  NewsFeed AI - Starting workflow")
    print("=" * 55)

    try:
        # ── Step 1: Plan (pick category) ─────────────────────────────────────
        plan = planner.plan()
        category = plan["category"]
        print(f"[Workflow] Selected category: {category}")

        # ── Step 2: Search ────────────────────────────────────────────────────
        articles, category_used = search.search(category)
        if not articles:
            print("[Workflow] No articles found in any category - aborting")
            return None

        print(f"[Workflow] {len(articles)} article(s) fetched for '{category_used}'")

        # ── Step 3: Filter duplicates ─────────────────────────────────────────
        existing_urls = _load_existing_urls()
        fresh_articles = filter_agent.filter(articles, existing_urls)

        if not fresh_articles:
            print("[Workflow] All fetched articles are duplicates - aborting")
            return None

        print(f"[Workflow] {len(fresh_articles)} new article(s) after dedup")

        # ── Step 4: Pick the first fresh article ──────────────────────────────
        raw_article = fresh_articles[0]
        print(f"[Workflow] Processing: {raw_article.get('title', '')}")

        # ── Step 5: Write (AI rewrite) ────────────────────────────────────────
        print("[Workflow] Generating AI article...")
        written = writer.rewrite(raw_article)

        # Merge original metadata into the written article
        written["url"] = raw_article.get("url", "")
        written["image"] = raw_article.get("image", "")
        written["source"] = raw_article.get("source", {})
        written["published_at"] = raw_article.get("publishedAt", "")

        # ── Step 6: Publish ───────────────────────────────────────────────────
        print("[Workflow] Saving article...")
        saved = publisher.publish(written, category_used)

        if saved:
            print(f"[Workflow] PUBLISHED: [{category_used}] {saved['title']}")
        else:
            print("[Workflow] WARNING: Article not saved (duplicate or missing URL)")

        print("=" * 55 + "\n")
        return saved

    except Exception as e:
        print(f"[Workflow] ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 55 + "\n")
        return None