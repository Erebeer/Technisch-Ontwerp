import csv
import urllib.request
import json
from flask import redirect, render_template, request, session
from functools import wraps

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
    api =  "https://opentdb.com/api.php?amount=10"
    webpage = list(urllib.request.urlopen(api))

    # Generates the questionset
    temp = json.loads(webpage[0].decode("utf-8"))['results']

    # Create lists of questions and correct answers
    all_questions = []
    correct_answers = []
    for x in temp:
        all_questions.append(x['question'])
    for x in temp:
        correct_answers.append(x['correct_answer'])

    # Combines both lists into a dict (key = question, value = correct answer)
    questionset = dict(zip(all_questions, correct_answers))

    return(questionset)