"""
PublisherAgent - Save a single processed article to output/news.json.

Handles:
- Duplicate prevention (by URL)
- Image validation + AI image generation fallback
- Full schema with all required fields
- Newest articles prepended (index 0)
"""

import json
import os
from datetime import datetime
from pathlib import Path

from tools.image_tool import generate_ai_image, is_valid_image_url

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
NEWS_FILE = OUTPUT_DIR / "news.json"


class PublisherAgent:

    def publish(self, article: dict, category: str) -> dict | None:
        """
        Publish a single article to news.json.

        Args:
            article:  Processed article dict from WriterAgent
            category: The category label (e.g. "AI Hub")

        Returns:
            The saved article dict, or None if it was a duplicate / had no URL.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # - Load existing news ────────────────────────────────────────────────
        existing_news = self._load_news()
        existing_urls = {item.get("url", "") for item in existing_news}

        article_url = article.get("url", "").strip()
        title = article.get("title", "")

        if not article_url:
            print("[PublisherAgent] Article has no URL - skipping")
            return None

        if article_url in existing_urls:
            print(f"[PublisherAgent] Duplicate skipped: {title}")
            return None

        # - Assign ID ─────────────────────────────────────────────────────────
        new_id = (max((a.get("id", 0) for a in existing_news), default=0) + 1)

        # - Image handling ────────────────────────────────────────────────────
        original_image = article.get("image", "")
        image_url, image_source = self._resolve_image(
            original_image, title, new_id
        )

        # - Build full article record ─────────────────────────────────────────
        now = datetime.now()
        source = article.get("source", "")
        if isinstance(source, dict):
            source = source.get("name", "")

        news_item = {
            "id": new_id,
            "category": category,
            "title": title,
            "summary": article.get("summary", ""),
            "description": article.get("description", ""),
            "image": image_url,
            "image_source": image_source,
            "url": article_url,
            "source": source,
            "published_at": article.get("published_at", ""),
            "created_date": now.strftime("%Y-%m-%d"),
            "created_time": now.strftime("%H:%M:%S"),
        }

        # - Prepend so newest appears first ───────────────────────────────────
        existing_news.insert(0, news_item)

        self._save_news(existing_news)

        print(f"[PublisherAgent] Article saved: [{category}] {title}")
        print(f"[PublisherAgent] Image source: {image_source} -> {image_url}")
        return news_item

    # - Image resolution ──────────────────────────────────────────────────────

    def _resolve_image(
        self, original_url: str, title: str, article_id: int
    ) -> tuple[str, str]:
        """
        Determine the image to use for the article.

        Returns:
            (image_url_or_path, image_source)
        """
        if original_url and is_valid_image_url(original_url):
            print("[PublisherAgent] Using original image")
            return original_url, "original"

        print("[PublisherAgent] Original image missing or invalid - generating AI image")
        path, source = generate_ai_image(title, article_id)
        return path, source

    # - File I/O ──────────────────────────────────────────────────────────────

    def _load_news(self) -> list:
        if NEWS_FILE.exists():
            try:
                with open(NEWS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_news(self, news: list) -> None:
        with open(NEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(news, f, indent=4, ensure_ascii=False)
        print(f"[PublisherAgent] news.json updated ({len(news)} total articles)")