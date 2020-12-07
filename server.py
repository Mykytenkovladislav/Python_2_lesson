import csv
import os
import sqlite3

import requests
from faker import Faker
from flask import Flask, render_template

app = Flask(__name__)
fake = Faker()

DATABASE = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def requirements_reading():
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'requirements.txt')
    requirements_data: list = []
    with open(data_file, "r") as file:
        for line in file.readlines():
            requirements_data.append(line.rstrip())
    return requirements_data


def generating_accounts(amount: int) -> dict:
    generated_accounts: dict = {}
    for _ in range(amount):
        account: str = fake.name()
        name_surname: list = account.split(' ')
        name_surname[1] = name_surname[1].lower() + '@gmail.com'
        generated_accounts[name_surname[0]] = name_surname[1]
    return generated_accounts


def reading_from_csv():
    with open('hw.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                            quoting=csv.QUOTE_MINIMAL)
        result: list = [0, 0, 0]
        for row in reader:
            if row == ['"Index"', ' "Height(Inches)"', ' "Weight(Pounds)"']:
                continue
            if not row:
                break
            result[0] = int(row[0])
            print(f'{result[0]=}')
            result[1] += float(row[1].strip(' '))
            print(f'{result[1]=}')
            result[2] += float(row[2].strip(' '))
            print(f'{result[2]=}')
        result = [(result[1] * 2.54) / result[0], (result[2] * 0.453592) / result[0]]
        return result


def get_amount_of_astronauts():
    r = requests.get('http://api.open-notify.org/astros.json')
    astronauts = r.json().get('number')
    return astronauts


@app.route('/')
def index():
    users = []
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT id,first_name, surname,email,age FROM customers"):
                users.append(row)
    return render_template("index.html", users=users)


@app.route('/requirements/')
def requirements():
    requirements_data = requirements_reading()
    return render_template('requirements.html', requirements_data=requirements_data)


@app.route('/generate-users/')
@app.route('/generate-users/<int:users_amount>')
def generate_users(users_amount=100):
    accounts = generating_accounts(users_amount)
    return render_template('generate-users.html', accounts=accounts)


@app.route('/mean/')
def mean():
    middle_weight_height = reading_from_csv()
    return render_template('mean.html', middle_weight_height=middle_weight_height)


@app.route('/space/')
def space():
    amount_of_astronauts = get_amount_of_astronauts()
    return render_template('space.html', amount_of_astronauts=amount_of_astronauts)


@app.route('/names/')
def names():
    first_names: list = []
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT COUNT(DISTINCT first_name) FROM customers"):
                first_names.append(row)
    amount_of_unique_first_names = len(first_names)
    return render_template("names.html",
                           amount_of_unique_first_names=amount_of_unique_first_names,
                           first_names=first_names)


@app.route('/tracks/')
def tracks():
    count = 0
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT COUNT (id) FROM tracks"):
                count = row[0]
    return render_template("tracks.html", count=count)


@app.route('/tracks/<genre>')
def tracks_genre(genre='Rock'):
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            genre_value = (genre,)
            qs = cursor.execute(f"SELECT COUNT (id) FROM tracks WHERE song_genre = ?", genre_value)
            count = qs.fetchone()
    return render_template("genre.html", genre=genre, count=count[0])


@app.route('/tracks-sec/')
def tracks_sec():
    title_and_duration = []
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            for row in cursor.execute(f"SELECT song_title, song_length FROM tracks"):
                title_and_duration.append(row)
    return render_template("tracks_sec.html", title_and_duration=title_and_duration)


@app.route('/tracks-sec/statistics/')
def tracks_sec_statistic():
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            qs = cursor.execute(f"SELECT AVG(song_length) FROM tracks")
            average_duration = qs.fetchone()
            qs = cursor.execute(f"SELECT SUM(song_length) FROM tracks")
            total_duration = qs.fetchone()
    return render_template("tracks_sec_statistic.html", total_duration=total_duration[0],
                           average_duration=average_duration[0])
