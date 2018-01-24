from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import helpers

app = Flask(__name__)
app.config['SECRET_KEY']="Your secret key"

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trivia.db")

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    # session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

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

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return error("No username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return error("No password")

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("verificationpassword"):
            return error("Verification does not match")

        hash = pwd_context.hash(request.form.get("password"))

        # Saves username to the database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",username=request.form.get("username"), hash = hash)

        if not result:
           return error("Just Error")

        # Keeps the registered user logged in()
        session["user_id"] = result

        # Goes to homepage
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/leaderboards", methods=["GET", "POST"])
def leaderboards():
    leaderboard = db.execute("SELECT * from users WHERE id= :id", id=1)
    return render_template("leaderboards.html", leaderboard = leaderboard, username = "Pietje")

@app.route("/question1", methods=["POST"])
def question1():
    return render_template("home.html")

@app.route("/play", methods=["GET", "POST"])

def question1():
    question = helpers.question1()
    return render_template("question1.html", question=question)


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
def logout():
    # Clear the session, forget user_id
    session.clear()

    # Go back to the homepage
    return render_template("logout.html")

if __name__ == "__main__":
    app.run