from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Set these as environment variables in Render dashboard
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # same as you set in Meta Webhook setup
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")  # your permanent system user token
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")  # from WhatsApp API dashboard

@app.route("/")
def home():
    return "WhatsApp Webhook is running!"

# Webhook verification
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403

# Webhook for incoming messages
@app.route("/webhook", methods=["POST"])
def incoming_message():
    data = request.get_json()

    print("Incoming message:", data)  # For debugging

    try:
        # Extract message details
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages", [])

        if messages:
            msg = messages[0]
            sender = msg["from"]  # WhatsApp number of sender
            text = msg["text"]["body"]  # Message text

            print(f"Message from {sender}: {text}")

            # Send reply
            send_whatsapp_message(sender, f"Hi! You said: {text}")

    except Exception as e:
        print("Error processing message:", e)

    return "EVENT_RECEIVED", 200

# Function to send a WhatsApp message
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message send status:", response.status_code, response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
