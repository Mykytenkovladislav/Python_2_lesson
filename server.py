import os

from flask import Flask, render_template

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'requirements.txt')

app = Flask(__name__)

WORDS = []
with open(data_file, "r") as file:
    for line in file.readlines():
        WORDS.append(line.rstrip())


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/requirements")
def search():
    return f'{ WORDS }'
