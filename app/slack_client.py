import requests
from typing import List

def send_to_slack(webhook_url: str, articles: List[dict]):
    message_title = "*🚀 Daily AI & Tech News*\n\n"

    if not articles:
        message_body = "📭 No new articles today."
        json_message = {"text": message + message_body}
    else:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message_title
                }
            },
            {
                "type": "divider"
            }
        ]

        for article in articles:
            message_body = (
                f"*{article.title}*\n"
                f"{article.summary}\n"
                f"💡 *Why it matters:* {article.why_it_matters}\n"
                f"📊 *Level:* {article.level}\n"
                f"🤖 *Interest:* {article.interest}\n"
                f"🔗 <{article.link}>\n\n-----\n\n"
            )

            blocks.extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_body
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "👍"},
                            "value": json.dumps({
                                "action": "like",
                                "title": article.title
                            })
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "👎"},
                            "value": json.dumps({
                                "action": "dislike",
                                "title": article.title
                            })
                        }
                    ]
                },
                {"type": "divider"}
            ])

    json_message = {"blocks": blocks}
    requests.post(webhook_url, json=json_message)
