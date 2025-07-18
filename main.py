from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Noroa Agent is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Example response
    return jsonify({"status": "received", "data": data})

if __name__ == "__main__":
    app.run(debug=True)
