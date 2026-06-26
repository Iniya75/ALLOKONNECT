from agents.search_agent import SearchAgent

search_agent = SearchAgent()

def generate_news():

    articles = search_agent.run()

    news = []

    for index, article in enumerate(articles[:10]):

        news.append({
            "id": index + 1,
            "title": article.get("title"),
            "summary": article.get("description"),
            "url": article.get("url"),
            "image": article.get("image"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt")
        })

    return news
