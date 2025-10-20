import sqlite3
import random
import datetime as dt
from pathlib import Path

def get_random_prediction():
    with open("predictions.txt", "r", encoding="utf-8") as f:
        all_of_them = [line.strip() for line in f if line.strip()]
    return random.choice(all_of_them)

DB_PATH_EXAM = Path("deadlines_exam.sqlite3")

def init_exam():
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute("CREATE TABLE IF NOT EXISTS exams(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, course TEXT NOT NULL, exam_type TEXT NOT NULL);")
    con.commit()
    con.close()

def add_exam(at: dt.datetime, course: str, exam_type: str):
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute("INSERT INTO exams(at, course, exam_type) VALUES(?, ?, ?)", (at.strftime("%Y-%m-%d %H:%M"), course, exam_type))
    con.commit()
    con.close()

def list_future_exams():
    now = dt.datetime.now()
    con = sqlite3.connect(DB_PATH_EXAM)
    cur = con.execute( "SELECT id, at, course, exam_type FROM exams WHERE at >= ? ORDER BY at ASC", (now.strftime("%Y-%m-%d %H:%M"),) )
    rows = cur.fetchall()
    con.close()
    return [{"id": r[0],
             "at": dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M"),
             "course": r[2],
             "exam_type": r[3]} for r in rows]

def homework_creating():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS homework(
                   id INTEGER PRIMARY KEY AUTOINCREMENT
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
    cursor.execute('INSERT into homework(subject, number, day, flag) VALUES(?, ?, ?)', (subject, number, day.strftime("%Y-%m-%d %H:%M"), flag=0))
    connection.commit()
    connection.close()

def homework_done()




