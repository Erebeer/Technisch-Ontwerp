from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers

db = SQL("sqlite:///trivia.db")

def displayquestion(number):
    # Select question out of the database and return for display
    questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=number)
    question = questiontemp[0]['question']
    return(question)

def displayanswer(number):
    # Select question out of the database and return for display
    answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=number)
    answer = answertemp[0]['answer']
    return(answer)

def updatescore(number):
    # user gives answer
    question = displayquestion(number)
    answer = displayanswer(number)
    givenanswer = str(request.form.to_dict('answer')['answer'])
    # If the answer is correct
    if givenanswer == answer:
        # Updates score in current game
        db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
        scoretemp = db.execute("SELECT score FROM score")
        # Sets variable
        score = scoretemp[0]["score"]
        return score
    else:
        # Updates score in current game
        db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
        scoretemp = db.execute("SELECT score FROM score")
        # Sets variable
        score = scoretemp[0]["score"]
        return score

def processquestion(num):
        question = displayquestion(num)
        answer = displayanswer(num)
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            question = displayquestion(num+1)
            answer = displayanswer(num+1)
            score = updatescore(num)
            return render_template("question02.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            question = displayquestion(num+1)
            answer = displayanswer(num+1)
            score = updatescore(num)
            return render_template("question02.html", score=score, question=question, answer=answer)

