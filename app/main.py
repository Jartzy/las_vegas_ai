from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")  # Explicitly set template directory

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return f"Received: {username} / {password}"  # Temporary response to test login

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Bind to all interfaces