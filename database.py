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


def taking_data_from_json():
    with open('music.json') as json_file:
        data: dict = json.load(json_file)
    for _ in data:
        artist_name: str = data['name']
        for album in data['albums']:
            album_title: str = album['title']
            for song in album['songs']:
                song_title: str = song['title']
                song_length: str = song['length']
                song_genre: str = song['genre']
                yield artist_name, album_title, song_title, song_length, song_genre


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
                artist VARCHAR(255) UNIQUE NOT NULL,
                album_title VARCHAR(255) UNIQUE NOT NULL,
                song_title VARCHAR(255) UNIQUE NOT NULL,
                song_length VARCHAR(255) UNIQUE NOT NULL,
                song_genre VARCHAR(255) UNIQUE NOT NULL)"""
            )
            for customer in generate_user(25):
                cursor.execute(
                    """INSERT INTO customers(username, email, age) VALUES (?, ?, ?)""",
                    customer
                )
            for track in generate_user(25):
                cursor.execute(
                    """INSERT INTO tracks(artist, album_title, song_title, song_length, song_genre) VALUES (?, ?, ?, 
                    ?, ?)""",
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
