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
    """Log user in."""
    # forget any user_id
    # session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return helpers.error("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return helpers.error("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return helpers.error("invalid username and/or password")

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
            return helpers.error("No username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return helpers.error("No password")

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("verificationpassword"):
            return helpers.error("Verification does not match")

        hash = pwd_context.hash(request.form.get("password"))

        # Saves username to the database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",username=request.form.get("username"), hash = hash)

        if not result:
           return helpers.error("Just Error")

        # Keeps the registered user logged in()
        session["user_id"] = result

        # Adds username to the leaderboards
        usernametemp = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
        username = usernametemp[0]["username"]
        db.execute("INSERT INTO leaderboards (username, total_games, total_score, avarage_score) VALUES (:username, :total_games, :total_score, :avarage_score)", username=username, total_games=0, total_score=0, avarage_score=0)

        # Goes to homepage
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
@helpers.login_required
def index():
    return render_template("index.html")

@app.route("/leaderboards", methods=["GET", "POST"])
@helpers.login_required
def leaderboards():
    leaderboards = db.execute("SELECT * from leaderboards")
    return render_template("leaderboards.html", leaderboard = leaderboards)

@app.route("/setup", methods=["GET", "POST"])
@helpers.login_required
def setup():
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

@app.route("/question01", methods=["GET", "POST"])
@helpers.login_required
def question01():
    num = 1
    if request.method == "POST":
        return trivia.processquestion(num)

    else:
        question = trivia.displayquestion(num)
        answer = trivia.displayanswer(num)
        score = 0
        return render_template("question01.html", question=question, answer = answer, score=score)

@app.route("/question02", methods=["GET", "POST"])
@helpers.login_required
def question02():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=2)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=2)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=3)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=3)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question03.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=3)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=3)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question03.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=2)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=2)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question02.html", question=question, answer = answer, score=score)

@app.route("/question03", methods=["GET", "POST"])
@helpers.login_required
def question03():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=3)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=3)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=4)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=4)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question04.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=4)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=4)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question04.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=3)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=3)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question03.html", question=question, answer = answer, score=score)

@app.route("/question04", methods=["GET", "POST"])
@helpers.login_required
def question04():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=4)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=4)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=5)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=5)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question05.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=5)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=5)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question05.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=4)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=4)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question04.html", question=question, answer = answer, score=score)

@app.route("/question05", methods=["GET", "POST"])
@helpers.login_required
def question05():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=5)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=5)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=6)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=6)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question06.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=6)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=6)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question06.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=5)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=5)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question05.html", question=question, answer = answer, score=score)

@app.route("/question06", methods=["GET", "POST"])
@helpers.login_required
def question06():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=6)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=6)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=7)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=7)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question07.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=7)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=7)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question07.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=6)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=6)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question06.html", question=question, answer = answer, score=score)

@app.route("/question07", methods=["GET", "POST"])
@helpers.login_required
def question07():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=7)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=7)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=8)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=8)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question08.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=8)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=8)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question08.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=7)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=7)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question07.html", question=question, answer = answer, score=score)


@app.route("/question08", methods=["GET", "POST"])
@helpers.login_required
def question08():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=8)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=8)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=9)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=9)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question09.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=9)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=9)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question09.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=8)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=8)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question08.html", question=question, answer = answer, score=score)

@app.route("/question09", methods=["GET", "POST"])
@helpers.login_required
def question09():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=9)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=9)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question10.html", score=score, question=question, answer=answer)
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return render_template("question10.html", score=score, question=question, answer=answer)

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=9)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=9)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question09.html", question=question, answer = answer, score=score)

@app.route("/question10", methods=["GET", "POST"])
@helpers.login_required
def question10():
    if request.method == "POST":
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
        answer = answertemp[0]['answer']
        givenanswer = str(request.form.to_dict('answer')['answer'])
        if givenanswer == answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = 100)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return redirect(url_for("results"))
        if givenanswer != answer:
            questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
            question = questiontemp[0]['question']
            answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
            answer = answertemp[0]['answer']
            givenanswer = str(request.form.to_dict('answer')['answer'])
            db.execute("UPDATE score SET score = score + :mutation", mutation = -50)
            scoretemp = db.execute("SELECT score FROM score")
            score = scoretemp[0]["score"]
            return redirect(url_for("results"))

    else:
        questiontemp = db.execute("SELECT question FROM game WHERE number=:number", number=10)
        question = questiontemp[0]['question']
        answertemp = db.execute("SELECT answer FROM game WHERE number=:number", number=10)
        answer = answertemp[0]['answer']
        scoretemp = db.execute("SELECT score FROM score")
        score = scoretemp[0]["score"]
        return render_template("question10.html", score=score, question=question, answer=answer)


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