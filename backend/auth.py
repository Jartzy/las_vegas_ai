import pyotp
import qrcode
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import get_db_connection, verify_user  # ✅ Import `verify_user` from database.py

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")  # ✅ Add URL prefix

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if session.get("authenticated"):  # ✅ If already logged in, redirect
        flash("You are already logged in.", "info")
        return redirect(url_for("dashboard"))  # ✅ Remove "main." prefix

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if verify_user(username, password):
            session["authenticated"] = True
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))  # ✅ Fix incorrect redirect
        else:
            flash("❌ Invalid username or password.", "danger")

    return render_template("login.html")  # ✅ Ensure login.html exists

@auth_bp.route("/logout")
def logout():
    """Log the user out."""
    session.pop("authenticated", None)
    flash("✅ Logged out successfully.", "info")
    return redirect(url_for("auth.login"))  # ✅ Redirect back to login page