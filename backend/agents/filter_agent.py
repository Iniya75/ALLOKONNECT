"""
FilterAgent — Deduplicate articles against already-saved URLs.
"""


class FilterAgent:

    def filter(self, articles: list, existing_urls: set = None) -> list:
        """
        Remove articles whose URLs already exist in news.json.

        Args:
            articles:      Raw articles from GNews
            existing_urls: Set of URLs already saved (from news.json)

        Returns:
            Filtered list with duplicates removed
        """
        if not existing_urls:
            return articles

        filtered = [
            a for a in articles
            if a.get("url", "") not in existing_urls
        ]

        removed = len(articles) - len(filtered)
        if removed:
            print(f"[FilterAgent] Removed {removed} duplicate(s)")

        return filtered