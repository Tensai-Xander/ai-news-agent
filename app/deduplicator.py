import json
import os
from typing import List
from app.models import Article

DATA_FILE = "data/seen_articles.json"

def load_seen():
    if not os.path.exists(DATA_FILE):
        return set()
    
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return set()
            return set(json.loads(content))
    except Exception:
        return set()

def save_seen(seen):
    with open(DATA_FILE, "w") as f:
        json.dump(list(seen), f)

def get_new_articles(articles: List[Article]) -> List[Article]:
    seen = load_seen()
    return [a for a in articles if a.link not in seen]

def mark_as_seen(articles: List[Article]):
    seen = load_seen()

    for article in articles:
        seen.add(article.link)

    save_seen(seen)
