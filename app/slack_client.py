import requests
from typing import List

def send_to_slack(webhook_url: str, articles: List[dict]):
    message = "*🚀 Daily AI & Tech News*\n\n"

    for i, article in enumerate(articles, 1):
        message += (
            f"*{i}. [{article['category']}] {article['title']}*\n"
            f"{article['summary']}\n"
            f"_Why it matters: {article['why_it_matters']}_\n"
            f"<{article['url']}>\n\n"
        )

    requests.post(webhook_url, json={"text": message})
