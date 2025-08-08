from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "my_verify_token"  # you choose this

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Webhook verification
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification token mismatch", 403

    elif request.method == "POST":
        # Handle incoming messages
        data = request.json
        print("Incoming message:", data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(port=5000)
