import os
import sqlite3
import json
from random import randint
from faker import Faker

fake = Faker(['en-US'])

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def generate_user(count=0):
    for _ in range(count):
        username = fake.name()
        email = f"{username.lower().replace(' ', '_')}@example.com"
        age = randint(18, 99)
        yield username, email, age


def reading_json_file() -> list:
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'music.json')
    with open(data_file, "r") as file:
        albums_data = file.readline()
        result_json = json.loads(str(albums_data))
        return result_json


def taking_data_from_json():
    data: list = reading_json_file()
    for artist in data:
        pass



def init_database():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS customers 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INTEGER NOT NULL DEFAULT 0)"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tracks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INTEGER NOT NULL DEFAULT 0)"""
            )
            for customers in generate_user(25):
                cursor.execute(
                    """INSERT INTO customers(username, email, age) VALUES (?, ?, ?)""",
                    customers
                )


def exec_query(query, *args):
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            qs = cursor.execute(query, args)
            results = qs.fetchall()
    return results


if __name__ == "__main__":
    init_database()
