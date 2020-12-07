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
        name_and_surname: list = username.split(' ', 1)
        email = f"{username.lower().replace(' ', '_')}@example.com"
        age = randint(18, 99)
        yield name_and_surname[0], name_and_surname[1], email, age


def taking_data_from_json():
    with open('music.json') as json_file:
        data: dict = json.load(json_file)
    for _ in data:
        artist_name: str = data['name']
        for album in data['albums']:
            album_title: str = album['title']
            for song in album['songs']:
                song_title: str = song['title']
                song_length_min_and_sec: list = song['length'].split(':')
                song_length: int = (int(song_length_min_and_sec[0]) * 60) + int(song_length_min_and_sec[1])
                song_genre: str = song['genre']
                yield artist_name, album_title, song_title, song_length, song_genre


def init_database():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS customers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INTEGER NOT NULL DEFAULT 0)"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tracks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist VARCHAR(255) NOT NULL,
                album_title VARCHAR(255) NOT NULL,
                song_title VARCHAR(255) NOT NULL,
                song_length INTEGER NOT NULL,
                song_genre VARCHAR(255) NOT NULL)"""
            )
            for customer in generate_user(25):
                cursor.execute(
                    """INSERT INTO customers(first_name, surname, email, age) VALUES (?, ?, ?, ?)""",
                    customer
                )
            for track in taking_data_from_json():
                # TODO Ask why it executes twice (duplicated records in table "tracks"
                cursor.execute(
                    """INSERT INTO tracks(artist, album_title, song_title, song_length, song_genre) VALUES 
                    (?, ?, ?, ?, ?)""",
                    track
                )


def exec_query(query, *args):
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            qs = cursor.execute(query, args)
            results = qs.fetchall()
    return results


if __name__ == "__main__":
    init_database()
