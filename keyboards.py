from telebot import types
from formatting import split_text_hw


def useful_urls_keyboards():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        "Перейти на вики ВШЭ", url='http://wiki.cs.hse.ru/Заглавная_страница')
    btn2 = types.InlineKeyboardButton("Узнать свою оценку по ДЗ Матана",
                                      url="https://docs.google.com/spreadsheets/d/1RUU6sk7MqPDfM5c7Uu3wdy90H7yl9ea5ekTYfSsctTU/edit?gid=845223336#gid=845223336")
    btn3 = types.InlineKeyboardButton("Узнать свою оценку по ДЗ Дискры",
                                      url="https://docs.google.com/spreadsheets/d/1bfa-SilQvN_j1BF2CJG2fl5Ei2yX693b/edit?usp=sharing&ouid=107086670525368017252&rtpof=true&sd=true")
    btn4 = types.InlineKeyboardButton("Узнать свою оценку по ИДЗ Линала",
                                      url="https://docs.google.com/spreadsheets/d/1RUU6sk7MqPDfM5c7Uu3wdy90H7yl9ea5ekTYfSsctTU/edit?gid=845223336#gid=845223336")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


def all_button_for_user():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Печенька!")
    btn2 = types.KeyboardButton("Weekly")
    btn3 = types.KeyboardButton("Ближайшие экзы")
    btn4 = types.KeyboardButton("Активировать напоминания")
    btn5 = types.KeyboardButton("Отключить напоминания")
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn1)
    return markup


def all_buttons_for_admin():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить дедлайн")
    btn2 = types.KeyboardButton("Добавить экз")
    btn3 = types.KeyboardButton("Печенька!")
    btn4 = types.KeyboardButton("Weekly")
    btn5 = types.KeyboardButton("Ближайшие экзы")
    markup.row(btn1, btn2)
    markup.row(btn4, btn5)
    markup.row(btn3)
    return markup


def homework_buttons(deadlines_list: list):
    markup = types.InlineKeyboardMarkup()
    for one in deadlines_list:
        text = f"{one['name_subject']} {one['type_hw'].upper()}-{one['number']} {one['time'].strftime('%d.%m.%y %H:%M')}"
        if one['flag']:
            text += "✅"
        btn = types.InlineKeyboardButton(
            f"{text}", callback_data=f"hw_done:{one['id']}")
        markup.add(btn)
    return markup
