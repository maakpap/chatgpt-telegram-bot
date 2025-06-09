import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PAWAN_API_KEY = os.environ.get("PAWAN_API_KEY")
BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        headers = {
            "Authorization": f"Bearer {PAWAN_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "pai-001-light-beta",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        }

        r = requests.post("https://api.pawan.krd/v1/chat/completions", headers=headers, json=body)
        reply = r.json().get("choices", [{}])[0].get("message", {}).get("content", "Er ging iets mis.")

        requests.post(f"{BASE_TELEGRAM_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}

@app.route("/")
def home():
    return "Bot draait op Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
