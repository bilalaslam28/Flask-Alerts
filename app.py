from flask import Flask, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def format_tv_time(raw_time):
    try:
        dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
        def ordinal(n):
            return f"{n}{'th' if 11<=n<=13 else {1:'st',2:'nd',3:'rd'}.get(n%10, 'th')}"
        return f"{ordinal(dt.day)} {dt.strftime('%B %Y at %H:%M')}"
    except:
        return raw_time

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    message = data.get("content", "")
    if "Time: " in message:
        try:
            raw_time = message.split("Time: ")[1].strip().replace("UTC", "").strip()
            formatted_time = format_tv_time(raw_time)
            message = message.replace(raw_time, formatted_time)
        except:
            pass
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
