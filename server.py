import os
from faker import Faker
from flask import Flask, render_template

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'requirements.txt')

app = Flask(__name__)
fake = Faker()

requirements: list = []

with open(data_file, "r") as file:
    for line in file.readlines():
        requirements.append(line.rstrip())


def generating_accounts(amount: int) -> dict:
    generated_accounts: dict = {}
    for _ in range(amount):
        account: str = fake.name()
        name_surname: list = account.split(' ')
        name_surname[1] = name_surname[1].lower() + '@gmail.com'
        generated_accounts[name_surname[0]] = name_surname[1]
    return generated_accounts


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/requirements/')
def requirements():
    return render_template('requirements.html', name=requirements)


@app.route('/generate-users/')
@app.route('/generate-users/<int:users_amount>')
def generate_users(users_amount=100):
    accounts = generating_accounts(users_amount)
    return render_template('generate-users.html', param=accounts)
