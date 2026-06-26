"""
SearchAgent — Fetch news for a category with automatic fallback.

If the primary category returns no articles, the agent iterates
through the remaining categories until it finds one that has news.
This guarantees the website is never left empty.
"""

from tools.gnews_tool import fetch_news_for_category, CATEGORY_QUERIES


class SearchAgent:

    def search(self, category: str) -> tuple[list, str]:
        """
        Search GNews for the given category. Falls back through all
        other categories if no results are found.

        Returns:
            (articles, category_used)
        """
        all_categories = list(CATEGORY_QUERIES.keys())

        # Put the requested category first, then cycle through the rest
        ordered = [category] + [c for c in all_categories if c != category]

        for cat in ordered:
            print(f"[SearchAgent] Searching category: {cat}")
            articles = fetch_news_for_category(cat)

            if articles:
                if cat != category:
                    print(
                        f"[SearchAgent] Primary '{category}' empty — "
                        f"using fallback '{cat}'"
                    )
                return articles, cat

        print("[SearchAgent] No articles found in any category")
        return [], category