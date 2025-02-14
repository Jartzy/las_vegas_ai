from flask import Flask, render_template, session, redirect, url_for
from database import get_db_connection
from auth import auth_bp  # ✅ Ensure this import works

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Register Blueprint BEFORE defining routes
app.register_blueprint(auth_bp)

def is_logged_in():
    return session.get("authenticated", False)

def log_event(level, source, message):
    """Insert a log entry into the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (level, source, message) VALUES (%s, %s, %s);",
        (level, source, message)
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")  # ✅ Root route should work fine
@app.route("/dashboard")  # ✅ Add /dashboard explicitly
def dashboard():
    if not is_logged_in():
        log_event("WARNING", "Access", "Unauthorized access attempt to dashboard")
        return redirect(url_for("auth.login"))  # ✅ This should now work!

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT timestamp, level, source, message FROM logs ORDER BY timestamp DESC LIMIT 50;")
    logs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)