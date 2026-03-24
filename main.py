from app.rss_collector import fetch_articles
from app.deduplicator import filter_new_articles
from app.openai_service import select_top_articles
from app.slack_client import send_to_slack
from app.config import SLACK_WEBHOOK_URL

def main():
    articles = fetch_articles()
    new_articles = filter_new_articles(articles)

    if not new_articles:
        top_articles = "No new articles today."
    else:
        top_articles = select_top_articles(new_articles)

    send_to_slack(SLACK_WEBHOOK_URL, top_articles)

if __name__ == "__main__":
    main()
