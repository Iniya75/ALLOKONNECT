from dotenv import load_dotenv
import os
import requests

load_dotenv()


CATEGORY_QUERIES = {
    "Gadgets": "latest gadgets technology devices",
    "AI Hub": "artificial intelligence AI machine learning",
    "Finance": "finance economy markets stocks",
    "World News": "world news global international",
    "Open Source": "open source software development",
    "Space Station": "space NASA exploration astronomy",
    "Features": "technology innovation future trends",
}


def fetch_news(query: str, max_results: int = 10) -> list:
    """Fetch articles from GNews API for a given query string."""

    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        print("[GNews] ERROR: GNEWS_API_KEY not set in .env")
        return []

    url = (
        f"https://gnews.io/api/v4/search?"
        f"q={requests.utils.quote(query)}"
        f"&lang=en"
        f"&max={max_results}"
        f"&sortby=publishedAt"
        f"&apikey={api_key}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        print(f"[GNews] Found {len(articles)} article(s) for query: '{query}'")
        return articles

    except requests.exceptions.Timeout:
        print(f"[GNews] Timeout fetching: {query}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"[GNews] Request error: {e}")
        return []

    except Exception as e:
        print(f"[GNews] Unexpected error: {e}")
        return []


def fetch_news_for_category(category: str) -> list:
    """Fetch articles using the category's mapped search query."""
    query = CATEGORY_QUERIES.get(category, category)
    return fetch_news(query)
