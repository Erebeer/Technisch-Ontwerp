from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run

#@app.route("/login", methods=["GET", "POST"])
#def login():
 #   return render_template("login.html")