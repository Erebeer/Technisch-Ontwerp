import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps

def error(message, topmessage="ERROR"):
    "Returns an error message"
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=topmessage, bottom=escape(message))