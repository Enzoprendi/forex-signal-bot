from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Error sending Telegram message:", e)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received:", data)

    pair = data.get("pair", "Unknown")
    side = data.get("side", "BUY")
    entry = data.get("entry", "N/A")
    tp = data.get("tp", "N/A")
    sl = data.get("sl", "N/A")

    message = f"""
💹 *{pair}* – *{side.upper()}* Signal  
📍 *Entry*: {entry}  
🎯 *TP*: {tp}  
🛡 *SL*: {sl}  
#forex #signals #LFX
"""
    send_telegram_message(message.strip())
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

