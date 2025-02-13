import psycopg2
import smtplib
import os
from email.mime.text import MIMEText

DB_CONFIG = {
    "dbname": "las_vegas_db",
    "user": "myuser",
    "password": "mypassword",
    "host": "db"
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVERS = ["your_email@gmail.com"]

def log_event(level, source, message, status_code=None, retry_count=0):
    """Logs an event in the database and sends an alert if critical."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """INSERT INTO logs (level, source, message, status_code, retry_count)
               VALUES (%s, %s, %s, %s, %s);"""
    cur.execute(query, (level, source, message, status_code, retry_count))

    conn.commit()
    cur.close()
    conn.close()

    if level == "CRITICAL":
        send_instant_alert(level, source, message)

def send_instant_alert(level, source, message):
    """Sends an immediate email alert for CRITICAL errors."""
    msg = MIMEText(f"🚨 {level} ALERT: {source} 🚨\n\n{message}")
    msg["Subject"] = f"URGENT: {source} Issue Detected"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECEIVERS)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
    server.quit()