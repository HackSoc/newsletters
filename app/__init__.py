from datetime import date
from typing import Generator, Tuple, List
import flask
import os

from operator import itemgetter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
EMAIL_DIR = os.path.join(BASE_DIR, "emails")
app = flask.Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.config["FLASK_DEBUG"] = True
app.config["FLASK_ENV"] = "development"


def list_emails() -> Generator[Tuple[date, str], None, None]:
    for filename in os.listdir(EMAIL_DIR):
        yield date.fromisoformat(filename[:10]), filename

@app.route("/email/<string:fn>.html")
def email(fn):
    return flask.send_from_directory(EMAIL_DIR, fn + ".html")

@app.route("/")
def index():
    emails = list(list_emails())
    emails.sort(key=itemgetter(0), reverse=True)
    return flask.render_template("index.html.jinja2", emails=emails, foo="bar")