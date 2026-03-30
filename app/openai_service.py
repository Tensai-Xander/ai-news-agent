from openai import AzureOpenAI
import json
from typing import List
from app.models import Article, Features
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    OUTPUT_ARTICLES_COUNT,
)
from app.user_profile import USER_PROFILE
from app.user_learning import get_user_preferences

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

user_prefs = get_user_preferences()

def parse_article(data: dict) -> Article:
    features_data = data.get("features", {})

    features = Features(
        has_code=bool(features_data.get("has_code", False)),
        is_deep_dive=bool(features_data.get("is_deep_dive", False)),
        is_tutorial=bool(features_data.get("is_tutorial", False)),
    )

    return Article(
        title=data.get("title", ""),
        link=data.get("link", ""),
        summary=data.get("summary", ""),
        why_it_matters=data.get("why_it_matters", ""),
        interest=data.get("interest", ""),
        features=features,
    )

def select_top_articles(articles: List[Article]) -> List[dict]:
    formatted_articles = []

    for a in articles:
        formatted_articles.append({
            "title": a.title,
            "link": a.link,
            "summary": a.summary
        })

    prompt = f"""
You are a senior software engineer and selecting high-quality technical articles.

Your profile:
- Interests: {", ".join(USER_PROFILE["interests"])}
- Exclude: {", ".join(USER_PROFILE["exclude"])}

From the following articles:
{json.dumps(formatted_articles, indent=2)}

Select the {OUTPUT_ARTICLES_COUNT} articles with this distribution:
- Around 1/3 about AI (LLMs, agents, AI tools)
- Around 1/3 about software architecture
- Around 1/3 about programming (frontend or backend, coding practices, frameworks, tutorials)

User feedback insights (learned from past behavior):
- Interest scores: {user_prefs["interest_scores"]}
- Feature preferences: {user_prefs["feature_scores"]}

Guidelines:
- Strongly prioritize topics with high positive scores
- Avoid topics with negative scores
- Prefer articles with features that have positive scores (e.g., deep dive, code)

STRICT RULES:
- Avoid duplicates or very similar topics
- Avoid low-value content (startup funding, marketing)
- Prioritize technical depth and relevance to your profile
- Even if the title does not explicitly match keywords, detect implicit relevance
- Only select articles written in English

Return a JSON OBJECT with a single key "articles" containing an array of objects.
Each object in the array must have:
- title
- summary (The provided summary is raw input. You must rewrite it into a concise 2-line summary)
- why_it_matters (1 line, be specific to your profile)
- interest (one of the user profile interests that is DIRECTLY and EXPLICITLY related to the article content)
- features:
  - has_code
  - is_deep_dive
  - is_tutorial
- link

Rules for features:
- has_code = true only if actual code is present
- is_deep_dive = true only if technical depth or internals
- is_tutorial = true only if step-by-step guide
- If unsure, set to false
"""

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        # clean ```` if any
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]

        data = json.loads(content)

        articles_list = data.get("articles", [])

        return [parse_article(a) for a in articles_list]
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from OpenAI. Raw content was:\n{content}")
        print("JSON Error:", e)
        return []
    except Exception as e:
        print("Error with OpenAI:", e)
        return []
