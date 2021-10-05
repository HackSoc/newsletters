import flask

from flask_frozen import Freezer

from datetime import date
from typing import Generator, Tuple, List
import os
from operator import itemgetter


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
EMAIL_DIR = os.path.join(BASE_DIR, "emails")
app = flask.Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.config["FLASK_DEBUG"] = True
app.config["FLASK_ENV"] = "development"
app.config["FREEZER_DESTINATION"] = os.path.join(BASE_DIR, "build")
app.config["FREEZER_DESTINATION_IGNORE"] = [".git*", "CNAME"]


def list_emails() -> Generator[Tuple[date, str], None, None]:
    for filename in os.listdir(EMAIL_DIR):
        yield {
            "filename": filename,
            "date": date.fromisoformat(filename[:10]),
            "title": filename[11:].removesuffix(".html").replace("-", " "),
        }


months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


@app.template_filter()
def format_date(d):
    if not isinstance(d, date):
        return d
    return f"{d.day} {months[d.month-1]} {d.year}"


@app.route("/email/<string:fn>")
def email(fn):
    return flask.send_from_directory(EMAIL_DIR, fn)


@app.route("/")
def index():
    emails = list(list_emails())
    emails.sort(key=itemgetter("date"), reverse=True)
    return flask.render_template("index.html.jinja2", emails=emails, foo="bar")


freezer = Freezer(app)


@app.cli.command("build")
def build():
    freezer.freeze()
