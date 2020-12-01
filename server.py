import os
from faker import Faker
from flask import Flask, render_template

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'requirements.txt')

app = Flask(__name__)
fake = Faker()

requirements: list = []
generated_accounts: dict = {}

with open(data_file, "r") as file:
    for line in file.readlines():
        requirements.append(line.rstrip())


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/requirements/')
def requirements():
    return render_template('requirements.html', name=requirements)


@app.route('/generate-users/')
@app.route('/generate-users/<int:users_amount>')
def generate_users(users_amount=100):
    for _ in range(users_amount):
        account: str = fake.name()
        name_surname: list = account.split(' ')
        name_surname[1] = name_surname[1].lower() + '@gmail.com'
        generated_accounts[name_surname[0]] = name_surname[1]
    return render_template('generate-users.html', param=generated_accounts)  # TODO Ask about cleaning after every entry

# @app.route('generate-users/')
# @app.route('/generate-users/<int:users_number>')
# def generate_users(amount=None):
#     if amount is None:
#         amount = 100
#     for _ in range(amount):
#         account: str = fake.name().lower()
#         account += "@gmail.com"
#         generated_accounts.append(account.replace(" ", ""))
#     return render_template ('generate-users.html', param=generated_accounts)
