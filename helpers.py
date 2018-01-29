import csv
import urllib.request
import json
from functools import wraps
import time
from cs50 import SQL
import html
from flask import Flask, flash, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import trivia



db = SQL("sqlite:///trivia.db")

def error(message, topmessage="ERROR"):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=topmessage, bottom=escape(message))

def generate():
    # Open the API
    api =  "https://opentdb.com/api.php?amount=11"
    webpage = list(urllib.request.urlopen(api))

    # Generates the questionset
    temp = json.loads(webpage[0].decode("utf-8"))['results']

    # Create lists of questions and correct answers
    all_questions = []
    correct_answers = []
    number = [x for x in range(11)]
    for x in temp:
        all_questions.append(x['question'])
    for x in temp:
        correct_answers.append(x['correct_answer'])

    # Combines both lists into a dict (key = question, value = correct answer)
    temp1 = list(zip(all_questions, correct_answers))
    questionset = dict(list(zip(number, temp1)))

    return(questionset)

def question():
    # Returns a random generated question with an answer
    questions = generate()
    question = html.unescape(questions[0][0])
    answer = html.unescape(questions[0][1])
    return ([question, answer])

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

def timerset():
    while True:
        seconds = input(">> ")
        try:
            stop_when = abs(int(seconds))
        except Keyboardinterrupt:
            break
        except:
            print("Not a number")

        while stop_when > 0:
            m, s = divmod(stop_when, 60)
            h, m = divmod(m, 60)
            time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
            print(time_left + "\r", end = "")
            time.sleep(1)
            stop_when -= 1

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
    result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",username=request.form.get("username"), hash = hash)
    if not result:
       return helpers.error("Just Error")
    # Keeps the registered user logged in()
    session["user_id"] = result
    # Adds username to the leaderboards
    usernametemp = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
    username = usernametemp[0]["username"]
    db.execute("INSERT INTO leaderboards (username, total_games, total_score, avarage_score) VALUES (:username, :total_games, :total_score, :avarage_score)", username=username, total_games=0, total_score=0, avarage_score=0)
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
        return redirect(url_for("index"))

