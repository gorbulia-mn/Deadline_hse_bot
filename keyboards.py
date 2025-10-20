from telebot import types


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
    btn4 = types.KeyboardButton("След. неделя")
    markup.row(btn2, btn4)
    markup.row(btn1, btn3)
    return markup


def all_buttons_for_admin():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить дедлайн")
    btn2 = types.KeyboardButton("Добавить экз")
    btn3 = types.KeyboardButton("Печенька!")
    btn4 = types.KeyboardButton("Weekly")
    btn5 = types.KeyboardButton("Ближайшие экзы")
    btn6 = types.KeyboardButton("След. неделя")
    markup.row(btn1, btn2)
    markup.row(btn4, btn6)
    markup.row(btn3, btn5)
    return markup
