# **Las Vegas AI - System Status & Documentation**

## **Project Overview**
Las Vegas AI is a **Flask-based system** that includes authentication, logging, AI-powered recommendations, and a React-based frontend.

### **Current Features Implemented**
✅ **Flask Backend:**
   - User authentication via login/logout system with **Two-Factor Authentication (2FA)**.
   - AI-powered recommendations using **machine learning**.
   - Logging system for tracking user actions and errors.
   - API routes to serve recommendations and user interactions.
   
✅ **PostgreSQL Database:**
   - Stores users (`users` table) with hashed passwords and 2FA secret.
   - Logs system events (`logs` table) for debugging & tracking.
   - Tracks user feedback on recommendations (`user_feedback` table).
   
✅ **React Frontend (Vite-based):**
   - **Authentication system** (Login, Logout, 2FA via OTP verification).
   - **Filters for recommendations** (category-based and location-based filtering).
   - **Recommendation display** with real-time API fetching.
   - **User feedback system** (Like, Dislike, Show More options).
   - **Chatbot UI for AI-powered responses**.
   
✅ **Dockerized Deployment:**
   - Uses `docker-compose` to manage Flask, PostgreSQL, and other services.
   - Persistent PostgreSQL storage via Docker volumes.
   - Nginx reverse proxy for production.
   
✅ **Security Measures:**
   - Passwords hashed using `bcrypt`.
   - Two-Factor Authentication (2FA) with Google Authenticator.
   - Unauthorized access attempts logged.
   - Secure API authentication.

---
## **Database Schema**

### **Users Table** (`users`)
| Column         | Type          | Description                      |
|---------------|--------------|----------------------------------|
| id            | SERIAL (PK)   | Unique user ID                   |
| username      | VARCHAR(255)  | Unique username                  |
| password_hash | TEXT          | Bcrypt-hashed password           |
| otp_secret    | TEXT          | Two-Factor Authentication secret |

### **Logs Table** (`logs`)
| Column     | Type          | Description                        |
|-----------|--------------|----------------------------------|
| id        | SERIAL (PK)   | Unique log ID                     |
| timestamp | TIMESTAMP     | Time event occurred (auto-set)    |
| level     | VARCHAR(50)   | Log level (INFO, WARNING, ERROR)  |
| source    | VARCHAR(255)  | Component that generated log      |
| message   | TEXT          | Log message                       |

### **User Feedback Table** (`user_feedback`)
| Column            | Type          | Description                                  |
|------------------|--------------|----------------------------------------------|
| id               | SERIAL (PK)   | Unique feedback ID                          |
| user_id          | UUID          | Foreign key to Users table                  |
| recommendation_id| UUID          | Foreign key to Recommendations table        |
| feedback_type    | VARCHAR(20)   | 'liked', 'disliked', or 'want_more'         |
| timestamp        | TIMESTAMP     | Time feedback was submitted                 |

---
## **System Usage**
### **Starting the Application**
To start the system with **Docker Compose:**
```bash
docker compose up --build -d
```
To restart the Flask container:
```bash
docker compose restart flask_app
```

### **Accessing the System**
- **Web Dashboard:** `http://localhost:5000`
- **Login Page:** `http://localhost:5000/auth/login`
- **Frontend Application:** `http://localhost:5173/`
- **Logs in Database:**
```bash
docker exec -it las_vegas_db psql -U myuser -d las_vegas_db -c "SELECT * FROM logs;"
```
- **Insert Test Log:**
```bash
docker exec -it las_vegas_db psql -U myuser -d las_vegas_db -c "INSERT INTO logs (level, source, message) VALUES ('INFO', 'System', 'Test log entry');"
```

---
## **Frontend Components & Pages**
### **Frontend Directory Structure**
```
frontend/
├── src/
│   ├── api/
│   │   ├── auth.ts  # Handles authentication API requests
│   │   ├── recommendations.ts  # Fetches recommendations from Flask API
│   ├── components/
│   │   ├── AttractionCard.tsx  # Displays an individual recommendation
│   │   ├── Filters.tsx  # Handles category-based filtering
│   ├── pages/
│   │   ├── Login.tsx  # Handles login & 2FA authentication
│   │   ├── Recommendations.tsx  # Displays AI-generated recommendations
│   │   ├── Chatbot.tsx  # UI for AI chatbot interaction
│   ├── App.tsx  # Main application entry point
```

### **Key Frontend Features**
✅ **Login & Authentication**
- Users can log in with **username/password**.
- If enabled, **2FA is required via OTP**.

✅ **Filters & Recommendations**
- Users can **filter recommendations** by category.
- API fetches **real-time recommendations** from Flask backend.

✅ **User Feedback System**
- Users can **Like, Dislike, or Request More** recommendations.
- Feedback is stored in the database and used to **improve AI recommendations**.

✅ **Chatbot Interface**
- Users can **ask the chatbot for recommendations**.
- Chatbot **learns from user interactions** and provides improved responses.

---
## **Next Steps**
🔹 **Finalize frontend state management for smoother API interactions.**
🔹 **Refine AI recommendations based on user behavior.**
🔹 **Optimize performance and caching for a faster experience.**

**Status:** ✅ Stable but continuously improving! 🚀
