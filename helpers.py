import csv
import urllib.request
import json
from flask import redirect, render_template, request, session
from functools import wraps
import time
from cs50 import SQL

db = SQL("sqlite:///trivia.db")

def error(message, topmessage="ERROR"):
    "Returns an error message"
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

def question1():
    questions = generate()
    question = questions[0][0]
    answer = questions[0][1]
    return ([question, answer])
def question2():
    questions = generate()
    question2 = questions[1][0]
    return question2
def question3():
    questions = generate()
    question3 = questions[2][0]
    return question3
def question4():
    questions = generate()
    question4 = questions[3][0]
    return question4
def question5():
    questions = generate()
    question5 = questions[4][0]
    return question5
def question6():
    questions = generate()
    question6 = questions[5][0]
    return question6
def question7():
    questions = generate()
    question7 = questions[6][0]
    return question7
def question8():
    questions = generate()
    question8 = questions[7][0]
    return question8
def question9():
    questions = generate()
    question9 = questions[8][0]
    return question9
def question10():
    questions = generate()
    question10 = questions[9][0]
    return question10

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

def deleteall():
    db.execute("DROP TABLE game")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
