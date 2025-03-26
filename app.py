import os
import sys
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helpers import apology, login_required
from contextlib import closing
import json
from flask_frozen import Freezer

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

@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

@app.route("/newgame", methods=["GET", "POST"])
@app.route("/newgame.html", methods=["GET", "POST"])  # Alias for .html
def newgame():
    """Begin Chess Game"""
    if request.method == "POST":
        # Process form data here if needed
        return redirect("/")
    else:
        pieces = {
            "R": "\u2656", "N": "\u2658", "B": "\u2657", "Q": "\u2655", "K": "\u2654", "P": "\u2659", "": "",
            "r": "\u265C", "n": "\u265E", "b": "\u265D", "q": "\u265B", "k": "\u265A", "p": "\u265F"
        }
        board = [
            [pieces["r"], pieces["n"], pieces["b"], pieces["q"], pieces["k"], pieces["b"], pieces["n"], pieces["r"]],
            [pieces["p"], pieces["p"], pieces["p"], pieces["p"], pieces["p"], pieces["p"], pieces["p"], pieces["p"]],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            [pieces["P"], pieces["P"], pieces["P"], pieces["P"], pieces["P"], pieces["P"], pieces["P"], pieces["P"]],
            [pieces["R"], pieces["N"], pieces["B"], pieces["Q"], pieces["K"], pieces["B"], pieces["N"], pieces["R"]]
        ]
        return render_template("newgame.html", pieces=pieces, board=board)

@app.route("/multi-chess/login", methods=["GET", "POST"])
@app.route("/multi-chess/login.html", methods=["GET", "POST"])  # Alias for .html
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
        return render_template("login.html")  # Corrected to use "login.html"

@app.route("/logout", methods=["GET"])  # Explicitly allow only GET
@app.route("/logout.html", methods=["GET"])  # Alias for .html
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])  # Alias for .html
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Validate form inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must retype password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username already exists
        rows = query_db("SELECT * FROM users WHERE username = ?", [username])
        if rows:
            return apology("username is already taken", 400)

        # Insert new user into the database
        try:
            hash = generate_password_hash(password)
            conn = get_db()
            conn.execute("INSERT INTO users (username, hash) VALUES(?, ?)", [username, hash])
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return apology("registration failed", 500)

        # Log the user in
        rows = query_db("SELECT id FROM users WHERE username = ?", [username])
        if rows and len(rows) > 0:
            session["user_id"] = rows[0]["id"]
        else:
            return apology("registration failed", 500)

        # Redirect to the home page
        return redirect("/")

    # Render the registration page
    else:
        return render_template("register.html")

@app.route("/creategame", methods=["GET", "POST"])
@app.route("/creategame.html", methods=["GET", "POST"])  # Alias for .html
@login_required
def creategame():
    """Create a new game"""
    if request.method == "POST":
        user_id = session["user_id"]
        initial_board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        conn = get_db()
        conn.execute("INSERT INTO games (creator_id, board, turn, move_index, status) VALUES (?, ?, ?, ?, ?)", [user_id, json.dumps(initial_board), 'white', 0, 'waiting'])
        conn.commit()
        conn.close()  # Close the database connection
        game = query_db("SELECT * FROM games WHERE creator_id = ? AND status = 'waiting'", [user_id], one=True)
        game_id = game["id"]
        return redirect(f"/playgame/{game_id}.html")  # Ensure .html extension in redirect
    else:
        return render_template("creategame.html")  # Corrected to use "creategame.html"

@app.route("/joingame/<int:game_id>", methods=["GET", "POST"])
@app.route("/joingame/<int:game_id>.html", methods=["GET", "POST"])  # Alias for .html
@login_required
def joingame(game_id):
    """Join an existing game"""
    game = query_db("SELECT * FROM games WHERE id = ?", [game_id], one=True)
    if not game:
        return apology("game not found", 404)

    if request.method == "POST":
        user_id = session["user_id"]
        if game["joiner_id"] is not None:
            return apology("game already joined", 403)

        conn = get_db()
        conn.execute("UPDATE games SET joiner_id = ?, status = 'in_progress' WHERE id = ?", [user_id, game_id])
        conn.commit()
        conn.close()  # Close the database connection
        return redirect("/playgame/{}".format(game_id))
    else:
        return render_template("joingame.html", game_id=game_id)

@app.route("/findgame", methods=["GET"])  # Explicitly allow only GET
@app.route("/findgame.html", methods=["GET"])  # Alias for .html
@login_required
def findgame():
    """Find games created by other players"""
    games = query_db("SELECT * FROM games WHERE status = 'waiting'")
    return render_template("findgame.html", games=games)

@app.route("/playgame/<int:game_id>", methods=["GET", "POST"])
@app.route("/playgame/<int:game_id>.html", methods=["GET", "POST"])  # Alias for .html
def playgame(game_id):
    """Play the game"""
    game = query_db("SELECT * FROM games WHERE id = ?", [game_id], one=True)
    pieces = { "R": "\u2656", "N": "\u2658", "B": "\u2657", "Q": "\u2655", "K": "\u2654", "P": "\u2659", "": "",
            "r": "\u265C", "n": "\u265E", "b": "\u265D", "q": "\u265B", "k": "\u265A", "p": "\u265F"
    }
    if not game:
        return apology("game not found", 404)

    if request.method == "POST":
        user_id = session["user_id"]
        if game["status"] != 'in_progress':
            return apology("game already ended", 403)
        if (game["turn"] == 'white' and user_id != game["creator_id"]) or (game["turn"] == 'black' and (game["joiner_id"] is None or user_id != game["joiner_id"])):
            return apology("not your turn", 403)

        board = json.loads(game["board"])
        turn = game["turn"]

        try:
            # Update the turn
            new_turn = 'black' if game["turn"] == 'white' else 'white'
            conn = get_db()
            conn.execute("UPDATE games SET board = ?, turn = ?, move_index = move_index + 1 WHERE id = ?", [json.dumps(board), new_turn, game_id])
            conn.commit()
            conn.close()  # Close the database connection
        except Exception as e:
            print(f"Error processing move: {e}")
            return apology("error processing move", 500)
        return redirect(f"/playgame/{game_id}")
    else:
        board = json.loads(game["board"])
        turn = game["turn"]
        return render_template("playgame.html", game=game, board=board, turn=turn, pieces=pieces)

@app.route("/update_game", methods=["POST"])  # Explicitly allow only POST
@login_required
def update_game():
    """Update the game state"""
    data = request.get_json()
    game_id = data['game_id']
    board = data['board']
    turn = data['turn']

    try:
        conn = get_db()
        conn.execute("UPDATE games SET board = ?, turn = ?, move_index = move_index + 1 WHERE id = ?", [json.dumps(board), turn, game_id])
        conn.commit()
        conn.close()  # Close the database connection
        return jsonify(success=True)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify(success=False, error=str(e))

freezer = Freezer(app)

@freezer.register_generator
def url_generator():
    yield '/'
    yield '/login.html'
    yield '/newgame.html'
    yield '/logout.html'
    yield '/register.html'
    yield '/creategame.html'
    yield '/findgame.html'
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        games = conn.execute("SELECT id FROM games").fetchall()
        for game in games:
            # Generate URLs for playgame and joingame with .html extension
            yield f'/playgame/{game["id"]}.html'
            yield f'/joingame/{game["id"]}.html'

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=8000, debug=True)