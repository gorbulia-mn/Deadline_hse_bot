import sqlite3
import random


def get_random_prediction():
    with open("predicitions.txt", "r", encoding="utf-8") as f:
        all_of_them = [line.strip() for line in f if line.strip()]
    return random.choice(all_of_them)
