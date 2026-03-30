from app.rss_collector import fetch_articles
from app.deduplicator import get_new_articles, mark_as_seen
from app.openai_service import select_top_articles
from app.slack_client import send_to_slack
from app.config import SLACK_WEBHOOK_URL

def main():
    articles = fetch_articles()
    new_articles = get_new_articles(articles)
    top_articles = select_top_articles(new_articles)

    print(top_articles)

    send_to_slack(SLACK_WEBHOOK_URL, top_articles)

    mark_as_seen(top_articles)

if __name__ == "__main__":
    main()
