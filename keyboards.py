from telebot import types


def useful_urls_keyboards():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        "Перейти на вики ВШЭ", url='http://wiki.cs.hse.ru/Заглавная_страница')
    btn2 = types.InlineKeyboardButton("Узнать свою оценку по ДЗ Дискры",
                                      url="https://docs.google.com/spreadsheets/d/1bfa-SilQvN_j1BF2CJG2fl5Ei2yX693b/edit?usp=sharing&ouid=107086670525368017252&rtpof=true&sd=true")
    markup.add(btn1)
    markup.add(btn2)
    return markup


def role_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Пользователь"),
               types.KeyboardButton("Админ"))
    return markup
