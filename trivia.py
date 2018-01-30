import urllib.request
import json
import html
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers

# The database where questions, users and scores are stored
db = SQL("sqlite:///trivia.db")

def generate():
    # Reads the API, Creates list of questions and answers, generates a question with answer

    # Open the API
    api = select_difficulty()
    print(api)
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
    questions = dict(list(zip(number, temp1)))

    # Returns a random generated question with an answer, not sensitive to capitals
    question = html.unescape(questions[0][0])
    answer = html.unescape(questions[0][1]).lower()
    return ([question, answer])

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

        # Return the next question
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
    # Sets the question
    question = displayquestion(num)

    # Sets the answer
    answer = displayanswer(num)

    # Sets the score
    score = 0

    # Determines the right questiontemplate
    template = "question0"+str(num)+".html"

    return render_template(template, question=question, answer = answer, score=score)

def show_leaderboard():
    # Select the leaderboard table
    leaderboards = db.execute("SELECT * from leaderboards ORDER BY avarage_score DESC")

    # Shows the leaderboard
    return render_template("leaderboards.html", leaderboard = leaderboards)

def select_difficulty():

    # Determines the chosen difficulty
    difficulty = str(request.form.get("difficulty"))

    # Determines the type of questions to be generated
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
        question_and_answer = generate()
        question = question_and_answer[0]
        answer = question_and_answer[1]
        number = x
        db.execute("INSERT INTO game (number, question, answer) VALUES(:number, :question, :answer)", number=number, question=question, answer=answer )
    return redirect(url_for("question01"))

def select_username():
    # Selects and returns the username
    usernametemp = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    username = usernametemp[0]['username']
    return username

def select_score():
    # Selects and returns the score
    scoretemp = db.execute("SELECT score FROM score")
    score = scoretemp[0]["score"]
    return score

def save_game():
    # Saves the game and adds it to the database
    score = select_score()
    username = select_username()
    return db.execute("INSERT INTO allgames (id, score, username) VALUES(:id, :score, :username)", id=session["user_id"], score=score, username=username)

def update_leaderboard():
    # Selects the username and score
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

    # Return the score with the results
    return render_template("results.html", score=score)