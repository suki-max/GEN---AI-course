from flask import Flask, request, jsonify
from model import get_answer

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_q = data.get("question", "").strip()
    if not user_q:
        return jsonify({"error": "No question provided"}), 400
    ans = get_answer(user_q)
    return jsonify(ans)

@app.route("/", methods=["GET"])
def home():
    return "Medical Chat API is running. POST /chat with {'question': '...'}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
