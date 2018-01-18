from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp


app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trivia.db")

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear

    # POST method required
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return "Error"

        # ensure password was submitted
        elif not request.form.get("password"):
            return "Error"

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("varificationpassword"):
            return "Error"
        hash = pwd_context.hash(request.form.get("password"))

        # Saves username to the database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",username=request.form.get("username"), hash = hash)

        if not result:
            return "Error"

        # Keeps the registered user logged in
        session["user_id"] = result

        # Goes to homepage
        return redirect(url_for("login"))

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run
