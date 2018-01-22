import csv
import urllib.request
import json
from flask import redirect, render_template, request, session
from functools import wraps
import time

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
    api =  "https://opentdb.com/api.php?amount=5"
    webpage = list(urllib.request.urlopen(api))

    # Generates the questionset
    temp = json.loads(webpage[0].decode("utf-8"))['results']

    # Create lists of questions and correct answers
    all_questions = []
    correct_answers = []
    number = [x for x in range(10)]
    for x in temp:
        all_questions.append(x['question'])
    for x in temp:
        correct_answers.append(x['correct_answer'])

    # Combines both lists into a dict (key = question, value = correct answer)
    temp1 = list(zip(all_questions, correct_answers))
    questionset = dict(list(zip(number, temp1)))

    return(questionset)

    def countdown(minutes):
       while minutes > 0:
            minutes = minutes - 1
            time.sleep(1)
            if minutes == 0:
                print("Time is up!")

minutes = int(input() * 60)
countdown(minutes)

