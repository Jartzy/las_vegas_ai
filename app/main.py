from flask import Flask, render_template, session, redirect, url_for
from database import get_db_connection
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this for security
app.register_blueprint(auth_bp)

def is_logged_in():
    """Checks if a user is logged in."""
    return "user" in session

@app.route("/")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT timestamp, level, source, message FROM logs ORDER BY timestamp DESC LIMIT 50;")
    logs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)