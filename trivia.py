from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers

# The database where questions, users and scores are stored
db = SQL("sqlite:///trivia.db")

def displayquestion(number):
    # Select question out of the database and return for display
    questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=number)
    question = questiontemp[0]['question']
    return(question)

def displayanswer(number):
    # Select answer out of the database and return for display
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
    # Displays question on the page
        question = displayquestion(num)
        answer = displayanswer(num)
        givenanswer = str(request.form.to_dict('answer')['answer'])

        # If the answer is right
        if givenanswer == answer:
            # If it is not the last question, display the next question. Else, display results.
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
                return redirect(url_for("results"))
            return render_template(template, score=score, question=question, answer=answer)

        # If the answer is wrong.
        if givenanswer != answer:
            # If it is not the last question, display the next question. Else, display results.
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
    # Gets the question, answer and score en puts it on the webpage
    question = displayquestion(num)
    answer = displayanswer(num)
    score = 0
    template = "question0"+str(num)+".html"
    return render_template(template, question=question, answer = answer, score=score)

def show_leaderboard():
    leaderboards = db.execute("SELECT * from leaderboards ORDER BY avarage_score DESC")
    return render_template("leaderboards.html", leaderboard = leaderboards)

def select_difficulty():
    difficulty = str(request.form.get("difficulty"))
    print(difficulty)
    if difficulty == "novice":
        api = "https://opentdb.com/api.php?amount=10&difficulty=easy"
    elif difficulty == "medium":
        api = "https://opentdb.com/api.php?amount=10&difficulty=medium"
    else:
        api = "https://opentdb.com/api.php?amount=10&difficulty=hard"
    return api


def create_game():
    # Makes sure all previously saved content has been deleted and resetted
    db.execute("DELETE FROM game")
    db.execute("DELETE FROM score")
    db.execute("INSERT INTO score (score) VALUES (:score)", score=0)

    # Fills the temporary table with questions
    for x in range(1, 11):
        question_and_answer = helpers.question()
        question = question_and_answer[0]
        answer = question_and_answer[1]
        number = x
        db.execute("INSERT INTO game (number, question, answer) VALUES(:number, :question, :answer)", number=number, question=question, answer=answer )
    return redirect(url_for("question01"))

def select_username():
    usernametemp = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    username = usernametemp[0]['username']
    return username

def select_score():
    scoretemp = db.execute("SELECT score FROM score")
    score = scoretemp[0]["score"]
    return score

def save_game():
    score = select_score()
    username = select_username()
    return db.execute("INSERT INTO allgames (id, score, username) VALUES(:id, :score, :username)", id=session["user_id"], score=score, username=username)

def update_leaderboard():
    username = select_username()
    score = select_score()

    # Updates the score
    oldscoretemp = db.execute("SELECT total_score FROM leaderboards WHERE username = :username", username=username)
    oldscore = oldscoretemp[0]["total_score"]
    oldgamestemp = db.execute("SELECT total_games FROM leaderboards WHERE username = :username", username=username)
    oldgames = oldgamestemp[0]["total_games"]
    newscore = oldscore + score
    newgames = oldgames + 1
    newavarage = int(newscore / newgames)

    # Updates the leaderboard
    db.execute("UPDATE leaderboards SET total_score = :newscore, total_games = :newgames, avarage_score= :newavarage WHERE username = :username", username=username, newscore=newscore, newgames=newgames, newavarage=newavarage)

    # Deletes questions, answers and scores
    helpers.deleteall()
    return render_template("results.html", score=score)