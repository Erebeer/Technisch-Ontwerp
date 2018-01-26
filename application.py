from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers
import trivia

app = Flask(__name__)
app.config['SECRET_KEY']="Your secret key"

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trivia.db")

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()
    if request.method == "POST":
        return helpers.login()
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return helpers.register()
    else:
        return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
@helpers.login_required
def index():
    return render_template("index.html")

@app.route("/leaderboards", methods=["GET", "POST"])
@helpers.login_required
def leaderboards():
    return trivia.show_leaderboard()

@app.route("/setup", methods=["GET", "POST"])
@helpers.login_required
def setup():
    return trivia.create_game()

@app.route("/question01", methods=["GET", "POST"])
@helpers.login_required
def question01():
    num = 1
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question02", methods=["GET", "POST"])
@helpers.login_required
def question02():
    num = 2
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question03", methods=["GET", "POST"])
@helpers.login_required
def question03():
    num = 3
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question04", methods=["GET", "POST"])
@helpers.login_required
def question04():
    num = 4
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question05", methods=["GET", "POST"])
@helpers.login_required
def question05():
    num = 5
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)


@app.route("/question06", methods=["GET", "POST"])
@helpers.login_required
def question06():
    num = 6
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question07", methods=["GET", "POST"])
@helpers.login_required
def question07():
    num = 7
    if request.method == "POST":
        return trivia.processquestion(num)

    else:
        return trivia.displaygame(num)


@app.route("/question08", methods=["GET", "POST"])
@helpers.login_required
def question08():
    num = 8
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question09", methods=["GET", "POST"])
@helpers.login_required
def question09():
    num = 9
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)

@app.route("/question10", methods=["GET", "POST"])
@helpers.login_required
def question10():
    num = 10
    if request.method == "POST":
        return trivia.processquestion(num)
    else:
        return trivia.displaygame(num)


@app.route("/results", methods=["GET"])
@helpers.login_required
def results():
    scoretemp = db.execute("SELECT score FROM score")
    score = scoretemp[0]["score"]
    usernametemp = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    username = usernametemp[0]['username']
    db.execute("INSERT INTO allgames (id, score, username) VALUES(:id, :score, :username)", id=session["user_id"], score=score, username=username)

    #Update leaderboard
    oldscoretemp = db.execute("SELECT total_score FROM leaderboards WHERE username = :username", username=username)
    print("TEST", oldscoretemp)
    oldscore = oldscoretemp[0]["total_score"]
    oldgamestemp = db.execute("SELECT total_games FROM leaderboards WHERE username = :username", username=username)
    oldgames = oldgamestemp[0]["total_games"]
    newscore = oldscore + score
    newgames = oldgames + 1
    newavarage = newscore / newgames
    db.execute("UPDATE leaderboards SET total_score = :newscore, total_games = :newgames, avarage_score= :newavarage WHERE username = :username", username=username, newscore=newscore, newgames=newgames, newavarage=newavarage)
    helpers.deleteall()
    return render_template("results.html", score=score)

def play():
    # Set score
    score = 0

    for x in questions:
        correct_answer = questions[x][1].lower()
        print(correct_answer)
        print(questions[x][0])
        print("Your Answer: ", end="")
        answer = request.form.get("answer")

        if answer == correct_answer:
            print("Correct!")
            score = score + 100
        elif answer == "pass":
            print("passed, you'll lose 50 points")
            score = score - 50
        else:
            score = score - 100
            print("Wrong, you'll lose 100 points")
        print("current score: ",score)

    print("Total Score: ", score)
    return render_template("game.html")


@app.route("/logout", methods=["GET", "POST"])
@helpers.login_required
def logout():
    # Clear the session, forget user_id
    session.clear()

    # Go back to the homepage
    return render_template("logout.html")

@app.route("/testlayout", methods=["GET", "POST"])
def testlayout():
    return render_template("testlayout.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run