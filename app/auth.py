import pyotp
import qrcode
from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from database import verify_user, get_db_connection

auth_bp = Blueprint("auth", __name__)

def get_otp_secret(username):
    """Retrieve user's 2FA secret from the database."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT otp_secret FROM users WHERE username = %s;"
    cur.execute(query, (username,))
    otp_secret = cur.fetchone()

    cur.close()
    conn.close()

    return otp_secret[0] if otp_secret else None

def generate_qr_code(username, otp_secret):
    """Generates a QR code for Google Authenticator."""
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
        name=username, issuer_name="Las Vegas AI Admin"
    )
    
    qr = qrcode.make(otp_uri)
    qr.save(f"static/qrcodes/{username}.png")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login with 2FA."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("auth.otp_verification"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("login.html")

@auth_bp.route("/otp", methods=["GET", "POST"])
def otp_verification():
    """Handles 2FA OTP verification."""
    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]
    otp_secret = get_otp_secret(username)

    if not otp_secret:
        flash("2FA Secret not found. Contact admin.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        otp_code = request.form["otp"]
        totp = pyotp.TOTP(otp_secret)

        if totp.verify(otp_code):
            session["authenticated"] = True
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid OTP code. Try again.", "danger")

    generate_qr_code(username, otp_secret)  # Generate QR Code for new users

    return render_template("otp.html", username=username)