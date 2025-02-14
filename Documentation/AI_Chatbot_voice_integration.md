🔹 Enhancing the AI Chatbot with Voice Interaction

To make the Las Vegas AI Chatbot more user-friendly, we’ll integrate Speech-to-Text (STT) and Text-to-Speech (TTS) capabilities.

📌 New Features
	1.	🎙️ Voice Input (Speech-to-Text)
	•	Users can speak instead of typing.
	•	The chatbot transcribes speech into text.
	•	Uses Web Speech API for browser-based recognition.
	2.	🗣️ AI Speaks (Text-to-Speech)
	•	AI responds vocally using browser speech synthesis.
	•	Users can hear recommendations instead of reading.

1️⃣ Updating the Chatbot UI

🔹 File: templates/chatbot.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Chat - Voice Enabled</title>
</head>
<body>
    <h1>Las Vegas AI Chat Assistant</h1>
    <div id="chatbox"></div>
    
    <input type="text" id="messageInput" placeholder="Ask something...">
    <button onclick="sendMessage()">Send</button>
    <button onclick="startListening()">🎙️ Speak</button>
    
    <script>
        function sendMessage() {
            const message = document.getElementById("messageInput").value;
            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("chatbox").innerHTML += 
                    `<p>User: ${message}</p><p>AI: ${data.response}</p>`;
                speakResponse(data.response);
            });
        }

        function startListening() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            
            recognition.onresult = (event) => {
                const speechText = event.results[0][0].transcript;
                document.getElementById("messageInput").value = speechText;
                sendMessage();
            };
            
            recognition.start();
        }

        function speakResponse(text) {
            const speech = new SpeechSynthesisUtterance();
            speech.text = text;
            speech.lang = 'en-US';
            window.speechSynthesis.speak(speech);
        }
    </script>
</body>
</html>

2️⃣ Updating the Chatbot API

🔹 File: chatbot.py

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

✅ Final Features Checklist

✔ Conversational Chatbot (AI Assistant)
✔ Location-Based Recommendations (GPS-based suggestions)
✔ Smart Booking & Google Calendar Integration
✔ Travel Itinerary Generation
✔ Voice Input (Speech-to-Text)
✔ AI Speech Output (Text-to-Speech)

📌 Updating Documentation for Beta Release

Project Name: AI-Powered Las Vegas Travel Assistant

📖 Overview

The Las Vegas AI Travel Assistant is a next-generation AI-powered recommendation system that allows users to:
	•	Chat with an AI assistant for recommendations.
	•	Receive personalized suggestions based on location & behavior.
	•	Book events & reservations, and sync with Google Calendar.
	•	Use voice interaction for hands-free communication.
	•	Plan a full itinerary dynamically.

📂 Final Project Structure

las_vegas_ai/
│── docker-compose.yml       # Docker for app & database
│── Dockerfile               # Defines Flask app container
│── requirements.txt         # Python dependencies
│── scheduled_tasks.py       # Periodic jobs
│── logs/                    # Stores log backups
│── static/
│   ├── qrcodes/             # Stores QR codes for 2FA
│── templates/               # HTML templates
│   ├── login.html           # Admin login
│   ├── otp.html             # 2FA authentication
│   ├── dashboard.html       # Admin log dashboard
│   ├── chatbot.html         # Voice-enabled chat UI
│   ├── itinerary.html       # Smart itinerary planner
│── app/                     
│   ├── main.py              # Flask App
│   ├── auth.py              # Authentication (Login, Logout, 2FA)
│   ├── fetcher.py           # API fetching logic
│   ├── scraper.py           # Web scraping logic
│   ├── alerts.py            # Logs & alert system
│   ├── database.py          # PostgreSQL connection
│   ├── recommendations.py   # AI Recommendation Engine
│   ├── tracking.py          # User Behavior Tracking
│   ├── chatbot.py           # Conversational AI Chatbot (Voice Enabled) 🔥
│   ├── location.py          # Location-Based Filtering 📍
│   ├── booking.py           # Google Calendar & Booking 📅
│   ├── ml_model.py          # Machine Learning for Personalized Suggestions 🤖
│   ├── feedback.py          # User Feedback System 👍👎

📅 Next Steps: Beta Release Checklist

✅ 1. Code Testing
	•	Functional testing for chat, recommendations, and booking.
	•	Ensure 2FA authentication works correctly.
	•	Test location-based filtering (works across different areas).

✅ 2. Deployment Readiness
	•	Final Docker build with all features.
	•	Deploy on AWS/DigitalOcean with Nginx reverse proxy.
	•	Enable SSL (HTTPS) for security.

✅ 3. Beta Testing Setup
	•	Invite test users to interact with the AI.
	•	Collect feedback on usability.
	•	Fix any critical bugs.

🚀 Final Question: What’s the Next Goal?

Would you like:
	1.	📲 A mobile app version of the chatbot (React Native / Flutter)?
	2.	🏆 Gamification features (user rewards, leaderboards)?
	3.	📡 API integrations (e.g., Uber for rides, OpenTable for direct bookings)?

Let me know, and we’ll continue expanding the system! 🚀