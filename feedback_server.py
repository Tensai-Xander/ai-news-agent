import os
import psycopg2
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def save_feedback(title: str, action: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO feedback (title, action, interest, has_code, is_deep_dive, is_tutorial)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (title, action, interest, has_code, is_deep_dive, is_tutorial)
    )

    conn.commit()
    cur.close()
    conn.close()

@app.post("/slack/feedback")
async def slack_feedback(request: Request):
    form = await request.form()

    print(form)

    payload = json.loads(form["payload"])

    action_data = payload["actions"][0]
    value = json.loads(action_data["value"])

    title = value["title"]
    action = value["action"]
    interest = value["interest"]

    features = value["features"]
    has_code = features["has_code"]
    is_deep_dive = features["is_deep_dive"]
    is_tutorial = features["is_tutorial"]

    print("TITLE:", title)
    print("ACTION:", action)
    print("INTEREST:", interest)
    print("HAS_CODE:", has_code)
    print("IS_DEEP_DIVE:", is_deep_dive)
    print("IS_TUTORIAL:", is_tutorial)

    save_feedback(
        title,
        action,
        interest,
        has_code,
        is_deep_dive,
        is_tutorial
    )

    return {"status": "ok"}