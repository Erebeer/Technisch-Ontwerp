from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers
import trivia


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
            if num != 10:
                question = displayquestion(num+1)
                answer = displayanswer(num+1)
                score = updatescore(num)
            else:
                question = displayquestion(num)
                answer = displayanswer(num)
                score = updatescore(num)
            if num != 10:
                template = "question0"+str(num + 1)+".html"
            else:
                template = "results.html"
            return render_template(template, score=score, question=question, answer=answer)
        if givenanswer != answer:
            if num != 10:
                question = displayquestion(num+1)
                answer = displayanswer(num+1)
                score = updatescore(num)
            else:
                question = displayquestion(num)
                answer = displayanswer(num)
                score = updatescore(num)
            if num != 10:
                template = "question0"+str(num + 1)+".html"
            else:
                template = "results.html"
            return render_template(template, score=score, question=question, answer=answer)

def displaygame(num):
    question = displayquestion(num)
    answer = displayanswer(num)
    score = 0
    template = "question0"+str(num)+".html"
    return render_template(template, question=question, answer = answer, score=score)

def show_leaderboard():
    leaderboards = db.execute("SELECT * from leaderboards")
    return render_template("leaderboards.html", leaderboard = leaderboards)

def create_game():
    db.execute("CREATE TABLE game ( number INTEGER, question TEXT, answer TEXT)")
    db.execute("CREATE TABLE score (score INTEGER)")
    db.execute("INSERT INTO score (score) VALUES (:score)", score=0)
    for x in range(1, 11):
        question_and_answer = helpers.question()
        question = question_and_answer[0]
        answer = question_and_answer[1]
        number = x
        db.execute("INSERT INTO game (number, question, answer) VALUES(:number, :question, :answer)", number=number, question=question, answer=answer )
    return render_template("setup.html")

def select_username():
    usernametemp = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    username = usernametemp[0]['username']
    return username

def select_score():
    scoretemp = db.execute("SELECT score FROM score")
    score = scoretemp[0]["score"]
    return score

