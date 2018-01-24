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

@app.route("/correct", methods=["GET", "POST"])
def correct():
    return render_template("correct.html")

@app.route("/wrong", methods=["GET", "POST"])
def wrong():
    return render_template("wrong.html")

@app.route("/setup", methods=["GET", "POST"])
def setup():
    db.execute("CREATE TABLE game ( number INTEGER, question TEXT, answer TEXT)")
    for x in range(1, 11):
        question_and_answer = helpers.question1()
        question = question_and_answer[0]
        answer = question_and_answer[1]
        number = x
        db.execute("INSERT INTO game (number, question, answer) VALUES(:number, :question, :answer)", number=number, question=question, answer=answer )
    return render_template("setup.html")

@app.route("/question01", methods=["GET", "POST"])
def question01():
    score = 0
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=1)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=1)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            score = score + 100
            return redirect(url_for("correct"))
        if givenanswer != answer:
            score = score - 50
            return render_template("wrong.html", answer=answer)


    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=1)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=1)
        answer = answertemp[0]['answer']
        return render_template("question01.html", question=question, answer = answer)

@app.route("/question02", methods=["GET", "POST"])
def question02():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question02.html", question=question, answer = answer)

@app.route("/question03", methods=["GET", "POST"])
def question03():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question03.html", question=question, answer = answer)

@app.route("/question04", methods=["GET", "POST"])
def question04():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question04.html", question=question, answer = answer)

@app.route("/question05", methods=["GET", "POST"])
def question05():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question05.html", question=question, answer = answer)

@app.route("/question06", methods=["GET", "POST"])
def question06():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question06.html", question=question, answer = answer)

@app.route("/question07", methods=["GET", "POST"])
def question07():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question07.html", question=question, answer = answer)

@app.route("/question08", methods=["GET", "POST"])
def question08():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question08.html", question=question, answer = answer)

@app.route("/question09", methods=["GET", "POST"])
def question09():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question09.html", question=question, answer = answer)

@app.route("/question10", methods=["GET", "POST"])
def question10():
    score = 0
    question_and_answer = helpers.question1()
    question = question_and_answer[0]
    answer = question_and_answer[1]
    givenanswer = request.form.get("answer")
    if givenanswer == answer:
        score = score + 100
    elif givenanswer == "pass":
        score = score - 50
    elif givenanswer != answer:
        score = score - 100

    return render_template("question10.html", question=question, answer = answer)

@app.route("/results", methods=["GET"])
def results():
    helpers.deleteall()
    return render_template("results.html")

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