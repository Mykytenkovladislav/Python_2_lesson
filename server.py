import csv
import os

from faker import Faker
from flask import Flask, render_template

app = Flask(__name__)
fake = Faker()


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
        result = [result[1] / result[0], result[2] / result[0]]
        return result


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/requirements/')
def requirements():
    requirements_data = requirements_reading()
    return render_template('requirements.html', param=requirements_data)


@app.route('/generate-users/')
@app.route('/generate-users/<int:users_amount>')
def generate_users(users_amount=100):
    accounts = generating_accounts(users_amount)
    return render_template('generate-users.html', param=accounts)


@app.route('/mean/')
def mean():
    middle_weight_height = reading_from_csv()
    return render_template('mean.html', param=middle_weight_height)
