Below is an expanded version of your project documentation that adds additional details on API endpoints, environment setup, testing, developer guidelines, and a future roadmap. You can integrate these sections into your documentation to further build out the project details.

Las Vegas AI - System Status & Documentation

Project Overview

Las Vegas AI is a Flask-based system that includes authentication, logging, AI-powered recommendations, and a React-based frontend. The project aims to provide AI-driven recommendations for Las Vegas attractions while ensuring secure user authentication and interaction tracking.

Key Features:
	•	✅ Secure Authentication: Login system with Two-Factor Authentication (2FA) using OTP.
	•	✅ AI-Powered Recommendations: Machine learning-based personalized suggestions.
	•	✅ User Feedback System: Users can like/dislike recommendations to refine AI predictions.
	•	✅ Chatbot Assistant: AI chatbot for travel-related questions and recommendations.
	•	✅ Logging & Monitoring: Tracks user actions, API calls, and errors.
	•	✅ Containerized Deployment: Uses Docker & Nginx for easy scalability.

Project Directory Structure

las_vegas_ai/
├── backend/                     # Flask Backend
│   ├── app.py                   # Main Flask application
│   ├── auth.py                  # Handles authentication & 2FA
│   ├── booking.py               # Booking & itinerary system
│   ├── chatbot.py               # AI chatbot logic
│   ├── database.py              # Database connection & queries
│   ├── fetcher.py               # Fetches recommendations via APIs
│   ├── location.py              # Location-based filtering logic
│   ├── main.py                  # Flask app entry point
│   ├── recommendations.py       # AI-powered recommendations
│   ├── scraper.py               # Web scraping for recommendations
│   ├── tracking.py              # Tracks user behavior & feedback
│   ├── alerts.py                # Logging & alert notifications
│   ├── templates/               # HTML templates for authentication
│   │   ├── chatbot.html         # Chatbot UI
│   │   ├── dashboard.html       # Admin dashboard
│   │   ├── itinerary.html       # User itinerary page
│   │   ├── login.html           # Login & 2FA UI
│   │   ├── otp.html             # 2FA verification
│   │   ├── recommendations.html # AI recommendations UI
│   ├── static/
│   │   ├── qrcodes/             # Stores generated QR codes for 2FA
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.ts          # Handles authentication API requests
│   │   │   ├── recommendations.ts # Fetches recommendations from Flask API
│   │   ├── components/
│   │   │   ├── AttractionCard.tsx  # Displays an individual recommendation
│   │   │   ├── Filters.tsx         # Handles category-based filtering
│   │   ├── pages/
│   │   │   ├── Login.tsx           # Handles login & 2FA authentication
│   │   │   ├── Recommendations.tsx # Displays AI-generated recommendations
│   │   │   ├── Chatbot.tsx         # UI for AI chatbot interaction
│   │   ├── App.tsx                 # Main application entry point
├── docker-compose.yml             # Defines backend & database containers
├── Dockerfile                   # Backend container build configuration
├── requirements.txt             # Python dependencies for Flask app
├── README.md                    # Project documentation

Database Schema

Events Table

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL CHECK (category IN ('Concert', 'Comedy', 'Theater', 'Festival', 'Sports', 'Other')),
    venue_id INT REFERENCES venues(id),
    date TIMESTAMP NOT NULL,
    price DECIMAL(10,2) CHECK (price >= 0),
    rating FLOAT CHECK (rating BETWEEN 0 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Venues Table

CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Recommendations Table

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL CHECK (category IN ('Restaurant', 'Bar', 'Nightclub', 'Museum', 'Outdoor', 'Shopping', 'Other')),
    venue_id INT REFERENCES venues(id),
    description TEXT,
    rating FLOAT CHECK (rating BETWEEN 0 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

User Interactions Table

CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recommendation_id INT REFERENCES recommendations(id) ON DELETE SET NULL,
    event_id INT REFERENCES events(id) ON DELETE SET NULL,
    action VARCHAR(20) CHECK (action IN ('viewed', 'liked', 'disliked', 'booked')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Reviews Table

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recommendation_id INT REFERENCES recommendations(id) ON DELETE SET NULL,
    event_id INT REFERENCES events(id) ON DELETE SET NULL,
    rating FLOAT CHECK (rating BETWEEN 0 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Next Steps
	1.	Migrate Database – Run these queries to create tables.
	2.	Insert Sample Data – Populate with test records.
	3.	Update API & Backend – Ensure queries & endpoints align.
	4.	Frontend Integration – Ensure UI fetches data correctly.

🚀 Project Status: Actively in development!

API Endpoints & Documentation

Authentication
	•	POST /api/auth/login
	•	Description: Authenticates user credentials.
	•	Payload:

{
  "username": "string",
  "password": "string"
}


	•	Response:
	•	Success (200 OK): Returns a temporary token for 2FA.
	•	Failure (401 Unauthorized): Invalid credentials.

	•	POST /api/auth/verify-otp
	•	Description: Verifies the OTP to complete authentication.
	•	Payload:

{
  "username": "string",
  "otp": "string"
}


	•	Response:
	•	Success (200 OK): Returns a JWT token.
	•	Failure (400 Bad Request): Invalid OTP.

	•	POST /api/auth/register
	•	Description: Registers a new user.
	•	Payload:

{
  "username": "string",
  "email": "string",
  "password": "string"
}


	•	Response:
	•	Success (201 Created): Registration successful.
	•	Failure (409 Conflict): User already exists.

Recommendations
	•	GET /api/recommendations
	•	Description: Fetches AI-powered recommendations.
	•	Query Parameters:
	•	category (optional): Filter recommendations by category.
	•	location (optional): Filter based on current location.
	•	Response:
	•	Success (200 OK): Returns a list of recommendations.
	•	POST /api/recommendations/feedback
	•	Description: Submits user feedback on a recommendation.
	•	Payload:

{
  "recommendation_id": "number",
  "action": "liked" | "disliked"
}


	•	Response:
	•	Success (200 OK): Feedback recorded.
	•	Failure (400 Bad Request): Invalid input.

Chatbot
	•	POST /api/chatbot/message
	•	Description: Processes user messages and returns AI chatbot responses.
	•	Payload:

{
  "message": "string"
}


	•	Response:
	•	Success (200 OK): Returns the chatbot’s reply.

Booking
	•	POST /api/booking
	•	Description: Books an event or adds an item to the user itinerary.
	•	Payload:

{
  "event_id": "number",
  "user_id": "UUID",
  "details": { /* additional booking details */ }
}


	•	Response:
	•	Success (201 Created): Booking confirmed.
	•	Failure (400 Bad Request): Invalid input or booking error.

Logging & Tracking
	•	POST /api/tracking
	•	Description: Logs user interactions for analytics.
	•	Payload:

{
  "user_id": "UUID",
  "action": "viewed" | "liked" | "disliked" | "booked",
  "entity": "event" | "recommendation",
  "entity_id": "number"
}


	•	Response:
	•	Success (200 OK): Log recorded.

Environment Setup & Deployment

Prerequisites
	•	Docker & Docker Compose (for containerized deployment)
	•	Python 3.8+ and pip (for the Flask backend)
	•	Node.js and npm/yarn (for the React frontend)

Local Development Setup
	1.	Clone the Repository:

git clone https://github.com/yourusername/las_vegas_ai.git
cd las_vegas_ai


	2.	Backend Setup:
	•	Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


	•	Install dependencies:

pip install -r requirements.txt


	•	Set environment variables:

export FLASK_APP=backend/app.py
export FLASK_ENV=development


	•	Run the Flask server:

flask run


	3.	Frontend Setup:
	•	Navigate to the frontend directory:

cd frontend


	•	Install dependencies:

npm install


	•	Start the React development server:

npm start



Docker Deployment
	•	Build the Containers:

docker-compose build


	•	Run the Containers:

docker-compose up


	•	Access the Application:
	•	The app should be available via the configured Nginx proxy.

Production Considerations
	•	Use a production-ready WSGI server (e.g., Gunicorn) for the Flask backend.
	•	Secure environment variables (e.g., with Docker secrets or a dedicated vault solution).
	•	Set up robust logging and monitoring (using tools such as Sentry or Prometheus).

Testing & Quality Assurance
	•	Unit Testing:
	•	Use pytest for backend unit tests.
	•	Integration Testing:
	•	Test API endpoints with tools like Postman or automated integration tests.
	•	Frontend Testing:
	•	Utilize Jest and React Testing Library for component and integration tests.
	•	CI/CD:
	•	Implement pipelines using GitHub Actions, Jenkins, or similar tools to automate testing and deployment.

Developer Guidelines
	•	Coding Standards:
	•	Follow PEP8 for Python code.
	•	Adhere to the Airbnb JavaScript/React style guide.
	•	Commit Message Conventions:
	•	Use Conventional Commits (e.g., feat:, fix:, docs:, refactor:, test:).
	•	Pull Request Workflow:
	•	Submit feature branches and include relevant tests/documentation updates.
	•	Issue Tracking:
	•	Use GitHub Issues to manage bugs, feature requests, and improvements.

Future Roadmap
	•	Mobile Application:
	•	Develop a mobile app using React Native for on-the-go access.
	•	Enhanced AI Capabilities:
	•	Integrate more advanced machine learning models and real-time recommendation updates.
	•	Social Integration:
	•	Implement social media logins and sharing functionalities.
	•	Multilingual Support:
	•	Localize the UI to support multiple languages.
	•	Real-time Communication:
	•	Utilize WebSockets for real-time chat updates and notifications.

Versioning & License
	•	Version: 1.0.0 (Initial release)
	•	License: MIT License (See the LICENSE file for details)

Contributing

Contributions are welcome! Please see the following guidelines:
	1.	Fork the repository.
	2.	Create a new branch for your feature or bug fix.
	3.	Commit your changes following the commit message conventions.
	4.	Submit a pull request with a detailed description of your changes.
	5.	Address any feedback from code reviews.

Troubleshooting & FAQs
	•	Database Connection Issues:
	•	Verify that your environment variables for the database connection are correctly set.
	•	2FA/OTP Problems:
	•	Ensure that your OTP generator (e.g., Google Authenticator) is synchronized with the server’s time and that the QR code is scanned correctly.
	•	Deployment Hiccups:
	•	Check your Docker and Nginx configurations if the app does not load as expected.
	•	General Debugging:
	•	Use the logs (configured in alerts.py and your container logs) to trace errors and troubleshoot issues.

This expanded documentation should help both new and experienced developers understand the system’s architecture, API endpoints, deployment procedures, and future plans. Feel free to further customize and expand each section as your project evolves.