from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trivia.db")

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    # session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return error("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return error("No username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return error("No password")

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("verificationpassword"):
            return error("Verification does not match")

        hash = pwd_context.hash(request.form.get("password"))

        # Saves username to the database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",username=request.form.get("username"), hash = hash)

        if not result:
           return error("Just Error")

        # Keeps the registered user logged in
        session["user_id"] = result

        # Goes to homepage
        return redirect(url_for("home"))

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run
