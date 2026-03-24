from openai import AzureOpenAI
import json
from typing import List
from app.models import Article
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    OUTPUT_ARTICLES_COUNT,
)
from app.user_profile import USER_PROFILE

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

def select_top_articles(articles: List[Article]) -> List[dict]:
    formatted_articles = [
        {"title": a.title, "url": a.link, "source": a.source}
        for a in articles
    ]

    prompt = f"""
You are an expert tech curator.

User profile:
- Interests: {", ".join(USER_PROFILE["interests"])}
- Exclude: {", ".join(USER_PROFILE["exclude"])}
- Level: {USER_PROFILE["level"]}
- Goal: {USER_PROFILE["goal"]}

From the following articles:
{formatted_articles}

Select the {OUTPUT_ARTICLES_COUNT} articles with this distribution:
- Around 1/3 about AI (LLMs, agents, AI tools, applied AI, developer usage of AI)
- Around 1/3 about software architecture
- Around 1/3 article about programming (frontend or backend, coding practices, frameworks, tutorials)

STRICT RULES:
- Prioritize technical depth and practical value
- Avoid duplicates or very similar topics
- Avoid low-value content (startup funding, marketing, hype)

Return JSON array with:
- category (AI, ARCHITECTURE, PROGRAMMING)
- title
- summary (2 lines max)
- why_it_matters (1 line)
- url

Return ONLY valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content

        return json.loads(content)
    except Exception as e:
        print("Error with OpenAI:", e)
        return []
