import json
from functools import wraps
from cs50 import SQL
import html
from flask import Flask, flash, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

db = SQL("sqlite:///trivia.db")

def error(message, topmessage="ERROR"):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=topmessage, bottom=escape(message))

def deleteall():
    # Deletes rows from the table made for the game
    db.execute("DELETE FROM game")
    db.execute("DELETE FROM score")
    db.execute("INSERT INTO score VALUES (:score)", score = 0)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def register():
    # ensure username was submitted
    if not request.form.get("username"):
        return helpers.error("No username")

    # ensure password was submitted
    elif not request.form.get("password"):
        return helpers.error("No password")

    # ensure password and verified password is the same
    elif request.form.get("password") != request.form.get("verificationpassword"):
        return helpers.error("Verification does not match")
    hash = pwd_context.hash(request.form.get("password"))

    # Saves username to the database
    result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"), hash = hash)
    if not result:
       return helpers.error("Just Error")

    # Keeps the registered user logged in()
    session["user_id"] = result
    # Adds username to the leaderboards

    usernametemp = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
    username = usernametemp[0]["username"]
    db.execute("INSERT INTO leaderboards (username, total_games, total_score, avarage_score) VALUES (:username, :total_games, :total_score, :avarage_score)",
                username=username, total_games=0, total_score=0, avarage_score=0)

    # Goes to homepage
    return redirect(url_for("index"))

def login():
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
        return redirect(url_for("home"))

def personalinfo():
    # Select username
    username = db.execute("SELECT username FROM leaderboards")

    # Select total games
    total_games = db.execute("SELECT total_games FROM leaderboards")

    # Select total score
    total_score = db.execute("SELECT total_score FROM leaderboards")

    # Select avarage score
    avarage_score = db.execute("SELECT avarage_score FROM leaderboards")

    # Retun personal information with all the attributes
    return render_template("personalinfo.html")

def delete_account():
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

    # Select username
    usernametemp = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
    username = usernametemp[0]["username"]

    # Deletes account from every database
    db.execute("DELETE FROM users WHERE id=:id", id=session["user_id"])
    db.execute("DELETE FROM leaderboards WHERE username=:username", username=username)

     # logs the user out
    session.clear()

    return render_template("home.html")

def change_password():

    # ensure password was submitted
    if not request.form.get("oldpassword"):
        return error("Must provide password")

    # ensure new password was submitted
    if not request.form.get("newpassword"):
        return error("Please enter new password")

    # ensure varification was submitted
    if not request.form.get("verificationpassword"):
        return error("Please enter a varification")

    # Select old password
    old = db.execute("SELECT hash FROM users WHERE id=:id", id=session["user_id"])
    print("hash: ",old[0]["hash"])

    # Ensure password is correct
    if not pwd_context.verify(request.form.get("oldpassword"), old[0]["hash"]):
        return error("Incorrect password")

    # Ensure new password matches the verification
    elif request.form.get("newpassword") != request.form.get("verificationpassword"):
        return error("New password doen't match varification")

    # Change password
    db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=pwd_context.hash(request.form.get("newpassword")), id=session["user_id"])

    # Goes to homepage
    return redirect