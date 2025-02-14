import openai
from flask import request, jsonify, session
from database import get_db_connection

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(user_id, message):
    """Uses GPT to generate a conversational response."""
    prompt = f"User: {message}\nAI:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    reply = response["choices"][0]["message"]["content"]
    log_chat_history(user_id, message, reply)
    return reply

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint to chat with the AI assistant."""
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 403

    user_id = session["user_id"]
    message = request.json.get("message")
    reply = generate_response(user_id, message)
    
    return jsonify({"response": reply})