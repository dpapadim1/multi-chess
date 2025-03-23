import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helpers import apology, login_required
from contextlib import closing

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database setup
DATABASE = os.path.join('src', 'database', 'multi_chess.db')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    try:
        conn = get_db()
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        user_id = session["user_id"]
        shares = query_db("SELECT symbol, number FROM owned_shares WHERE user_id = ?", [user_id])
        row = query_db("SELECT cash FROM users WHERE id = ?", [user_id], one=True)

        cash = row["cash"]
        total = cash
        for share in shares:
            share["price"] = 1234.
            share["total"] = 100. * share["number"]
            total += share["total"]
        return render_template("index2.html", shares=shares, cash=cash, total=total)

    else:
        return render_template("index.html")

@app.route("/newgame", methods=["GET", "POST"])
def newgame():
    """Begin Chess Game"""
    if request.method == "POST":
        # Process form data here if needed
        return redirect("/")
    else:
        return render_template("newgame.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", [request.form.get("username")])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must retype password", 400)

        # Ensure password confirmation is the same with password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        # Query database for username
        username = request.form.get("username")
        rows = query_db("SELECT * FROM users WHERE username = ?", [username])

        # Ensure username is not already taken
        if len(rows) != 0:
            return apology("username is already taken", 400)

        hash = generate_password_hash(request.form.get("password"))
        conn = get_db()
        conn.execute("INSERT INTO users (username, hash) VALUES(?, ?)", [username, hash])
        conn.commit()

        # Remember which user has logged in
        rows = query_db("SELECT id FROM users WHERE username = ?", [username])
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)