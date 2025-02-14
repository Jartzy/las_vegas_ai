# **Las Vegas AI - System Status & Documentation**

## **Project Overview**
Las Vegas AI is a **Flask-based system** that includes authentication, logging, and a simple dashboard for tracking system events.

### **Current Features Implemented**
✅ **Flask App Setup:**
   - User authentication via login/logout system.
   - Blueprint-based architecture (`auth.py`).
   - Logs system activity (e.g., user logins, unauthorized access attempts).
   
✅ **PostgreSQL Database:**
   - Stores users (`users` table) with hashed passwords.
   - Logs system events (`logs` table) for debugging & tracking.
   
✅ **Dockerized Deployment:**
   - Uses `docker-compose` to manage Flask, PostgreSQL, and other services.
   - Persistent PostgreSQL storage via Docker volumes.
   
✅ **Security Measures:**
   - Passwords hashed using `bcrypt`.
   - Unauthorized access attempts logged.
   - Sessions managed securely with Flask sessions.

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
- **Logs in Database:**
```bash
docker exec -it las_vegas_db psql -U myuser -d las_vegas_db -c "SELECT * FROM logs;"
```
- **Insert Test Log:**
```bash
docker exec -it las_vegas_db psql -U myuser -d las_vegas_db -c "INSERT INTO logs (level, source, message) VALUES ('INFO', 'System', 'Test log entry');"
```

---
## **Next Steps**
🔹 **Pause further database features** until the core site is established.
🔹 **Revisit logs & authentication** after site foundation is solid.
🔹 **Enhance user roles & permissions** in the future.

**Status:** ✅ Stable but needs expansion!

