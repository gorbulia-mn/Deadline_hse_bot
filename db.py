import sqlite3
import random
import datetime as dt
from pathlib import Path

DB_PATH_EXAM = Path("deadlines_exam.sqlite3")


def get_random_prediction():
    with open("predictions.txt", "r", encoding="utf-8") as f:
        all_of_them = [line.strip() for line in f if line.strip()]
    return random.choice(all_of_them)


def init_exam():
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute("CREATE TABLE IF NOT EXISTS exams(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, course TEXT NOT NULL, exam_type TEXT NOT NULL);")
    con.commit()
    con.close()


def add_exam(at: dt.datetime, course: str, exam_type: str):
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute("INSERT INTO exams(at, course, exam_type) VALUES(?, ?, ?)",
                (at.strftime("%Y-%m-%d %H:%M"), course, exam_type))
    con.commit()
    con.close()


def list_future_exams():
    now = dt.datetime.now()
    con = sqlite3.connect(DB_PATH_EXAM)
    cur = con.execute("SELECT id, at, course, exam_type FROM exams WHERE at >= ? ORDER BY at ASC",
                      (now.strftime("%Y-%m-%d %H:%M"),))
    rows = cur.fetchall()
    con.close()
    return [{"id": r[0],
             "at": dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M"),
             "course": r[2],
             "exam_type": r[3]} for r in rows]


# def homework_done():
#     pass


def init_hw():
    conn = sqlite3.connect('hw_database.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS my_homework(id INTEGER PRIMARY KEY AUTOINCREMENT, name_subject TEXT NOT NULL, type_hw TEXT NOT NULL, number INTEGER, date_dd TEXT NOT NULL, flag_completed INTEGER NOT NULL DEFAULT 0)')
    conn.commit()
    cur.close()
    conn.close()


def add_hw(sub: str, t: str,  n: int, date: dt.datetime, f: int = 0):
    conn = sqlite3.connect('hw_database.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO my_homework(name_subject, type_hw, number, date_dd, flag_completed) VALUES(?, ?, ?, ?, ?)',
                (sub, t, n, date.strftime("%d.%m.%y %H:%M"), f))
    conn.commit()
    cur.close()
    conn.close()


def list_future_hw():
    time_now = dt.datetime.now()
    conn = sqlite3.connect('hw_database.sql')
    cur = conn.cursor()
    cur.execute('SELECT id, type_hw, name_subject, number, date_dd, flag_completed FROM my_homework WHERE date_dd >= ? ORDER BY date_dd ASC',
                (time_now.strftime("%d.%m.%y %H:%M"),))
    all_hw = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": one[0], "type_hw": one[1], "name_subject": one[2], "number": one[3], "time": dt.datetime.strptime(one[4], "%d.%m.%y %H:%M"), "flag": one[5]} for one in all_hw]


def init_users():
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute('CREATE TABLE IF NOT EXISTS users(chat_id INTEGER PRIMARY KEY, flag INTEGER NOT NULL DEFAULT 0)')
    con.commit()
    con.close()

def add_user(chat_id: int):
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute('INSERT OR IGNORE INTO users(chat_id) VALUES (?)', (chat_id,))
    con.commit()
    con.close()

def set_user_flag(chat_id: int, value: int):
    con = sqlite3.connect(DB_PATH_EXAM)
    con.execute('UPDATE users SET flag=? WHERE chat_id=?', (value, chat_id))
    con.commit()
    con.close()

def list_users_flag() -> list[int]:
    con = sqlite3.connect(DB_PATH_EXAM)
    rows = [r[0] for r in con.execute('SELECT chat_id FROM users WHERE flag=1').fetchall()]
    con.close()
    return rows
