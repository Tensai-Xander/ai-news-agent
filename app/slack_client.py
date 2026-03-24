import requests
from typing import List

def send_to_slack(webhook_url: str, articles: List[dict]):
    message = "*🚀 Daily AI & Tech News*\n\n"

    for i, article in enumerate(articles, 1):
        message += (
            f"*{article['title']}*\n"
            f"{article['summary']}\n"
            f"💡 *Why it matters:* {article['why_it_matters']}\n"
            f"🎯 *Level:* {article['level']}\n"
            f"🤖 *Interest:* {article['interest']}\n"
            f"<{article['url']}>\n\n-----\n\n"
        )

    requests.post(webhook_url, json={"text": message})
