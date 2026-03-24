import os
from dotenv import load_dotenv

load_dotenv()

RSS_FEEDS = [
    # Architecture / system design
    {"name": "MartinFowler", "url": "https://martinfowler.com/feed.atom"},
    {"name": "ByteByteGo", "url": "https://blog.bytebytego.com/feed"},

    # General tech
    {"name": "HackerNews", "url": "https://hnrss.org/frontpage"},

    # Programming
    {"name": "Baeldung", "url": "https://www.baeldung.com/feed"},
    {"name": "FrontendMasters", "url": "https://frontendmasters.com/blog/feed/"},
]

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

MAX_ARTICLES_PER_FEED = 10
OUTPUT_ARTICLES_COUNT = 6
