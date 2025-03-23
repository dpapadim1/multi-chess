import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    """Start a chess game"""

    if request.method == "POST":
        return render_template("index2.html", shares=shares, cash=usd(cash), total=usd(total))
    else:
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)


@app.route("/newgame", methods=["GET", "POST"])
def newgame():
    """Begin Chess Game"""
    if request.method == "POST":
        # Process form data here if needed
        return redirect("/")
    else:
        return render_template("newgame.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)