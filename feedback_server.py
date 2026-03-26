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
        INSERT INTO feedback (title, action)
        VALUES (%s, %s)
        """,
        (title, action)
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

    action = value["action"]
    title = value["title"]

    print("ACTION:", action)
    print("TITLE:", title)

    save_feedback(title, action)

    return {"status": "ok"}