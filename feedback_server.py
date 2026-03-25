from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/slack/feedback")
async def slack_feedback(request: Request):
    form = await request.form()

    print(form)
    
    payload = json.loads(form["payload"])

    action = payload["actions"][0]
    value = json.loads(action["value"])

    print("ACTION:", value["action"])
    print("TITLE:", value["title"])

    return {"status": "ok"}