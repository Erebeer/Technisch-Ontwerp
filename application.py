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

@app.route('/', methods =["GET"])
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
    if request.method == "POST":
        # Selects difficulty, makes sure the right types of questions are generated
        difficulty = request.form.get("difficulty")
        api = trivia.select_difficulty()
        # Creates and starts the game
        return trivia.create_game()
    else:
        return render_template("index.html")

@app.route("/leaderboards", methods=["GET", "POST"])
@helpers.login_required
def leaderboards():
    return trivia.show_leaderboard()

@app.route("/question01", methods=["GET", "POST"])
@helpers.login_required
def question01():
    num = 1
    if request.method == "POST":
        # Shows and process all of the questions
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
    # Get the right username and score
    username = trivia.select_username()
    score = trivia.select_score()
    # Saves the game
    trivia.save_game()
    #Update leaderboard and show the result
    return trivia.update_leaderboard()

@app.route("/answers", methods=["GET"])
@helpers.login_required
def answers():
    answers = db.execute("SELECT * from game")
    return render_template("answers.html", game=answers)

@app.route("/logout", methods=["GET", "POST"])
@helpers.login_required
def logout():
    # Logs the user out
    session.clear()
    # Go back to the homepage
    return render_template("logout.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/settings", methods=["GET"])
@helpers.login_required
def settings():
    return render_template("settings.html")

@app.route ("/personalinfo", methods=["GET"])
@helpers.login_required
def personalinfo():
    return helpers.personalinfo()

@app.route ("/deleteaccount", methods=["GET", "POST"])
@helpers.login_required
def deleteaccount():
    return render_template("deleteaccount.html")

@app.route ("/confirmdelete", methods=["GET", "POST"])
@helpers.login_required
def confirmdelete():
    if request.method == "POST":
        helpers.delete_account()
        return redirect(url_for("home"))
    else:
        return render_template("confirmdelete.html")
    return render_template("confirmdelete.html")

@app.route ("/changepassword", methods=["GET", "POST"])
@helpers.login_required
def changepassword():
    if request.method == "POST":
        return helpers.change_password()
    else:
        return render_template("changepassword.html")

@app.route("/quit", methods = ["GET"])
def quit():
    return render_template("quit.html")

if __name__ == "__main__":
    app.run