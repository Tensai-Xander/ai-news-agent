import os
from dotenv import load_dotenv

load_dotenv()

RSS_FEEDS = [
    # Architecture / system design
    {"name": "MartinFowler", "link": "https://martinfowler.com/feed.atom"},
    {"name": "ByteByteGo", "link": "https://blog.bytebytego.com/feed"},

    # General tech
    {"name": "HackerNews", "link": "https://hnrss.org/frontpage"},

    # Programming
    {"name": "Baeldung", "link": "https://www.baeldung.com/feed"},
    {"name": "FrontendMasters", "link": "https://frontendmasters.com/blog/feed/"},
]

BEDROCK_API_KEY = os.getenv("BEDROCK_API_KEY")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")
BEDROCK_REGION = os.getenv("BEDROCK_REGION")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

MAX_ARTICLES_PER_FEED = 10
OUTPUT_ARTICLES_COUNT = 6
DECAY_DAYS = 14