import feedparser
from typing import List
from app.models import Article
from app.config import RSS_FEEDS, MAX_ARTICLES_PER_FEED

def fetch_articles() -> List[Article]:
    articles = []

    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed["url"])

        for entry in parsed.entries[:MAX_ARTICLES_PER_FEED]:
            articles.append(
                Article(
                    title=entry.title,
                    link=entry.link,
                    source=feed["name"]
                )
            )

    return articles
