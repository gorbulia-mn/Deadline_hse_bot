import sqlite3
import random


def get_random_prediction():
    with open("predictions.txt", "r", encoding="utf-8") as f:
        all_of_them = [line.strip() for line in f if line.strip()]
    return random.choice(all_of_them)

def homework_creating():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS homework(
                   subject TEXT NOT NULL,
                   number INTEGER,
                   day TEXT,
                   flag, BLOB
                   )
                   ''')
    connection.commit()
    connection.close()

def homework_adding(subject, number, day, flag=0):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE ')




