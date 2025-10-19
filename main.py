import telebot
from telebot import types
from dotenv import load_dotenv
import os
import sqlite3 # подключаемся к базе данных

# Загружаем .env из текущей папки
load_dotenv()

# Читаем переменную
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверим, что всё работает
# print("Бот токен:", BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)  # TeleBot это класс


# это декоратор от телебота(обращаемся к нашему боту), который на вход \
# получает список обрабатываемых им команд(но есть и другие аргументы), \
# пишутся команды без /; важно, что нужно написать commands=,\
# так как это kwargs
@bot.message_handler(commands=['start'])
# название функции может быть любым, message содержит всю информацию о \
# пользователе и о данном чате(к информации обращаемся по атрибутам)
def main(message):  # ПЕРЕДЕЛАТЬ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пользователь")
    btn2 = types.KeyboardButton("Админ")
    markup.row(btn1, btn2)
    # send_message это метод для отправки сообщений от бота, первый аргумент \
    # это id чата с пользователем, вторым аргументом сам текст, но опять же \
    # есть и другие аргументы(дофига); chat это класс, имеющий такие атрибуты \
    # как id, username, first_name, last_name, photo и так далее
    bot.send_message(
        message.chat.id, "<b>Привет</b>! Выбери, кем ты являешься для этого бота:", parse_mode='html', reply_markup=markup)
    # ВАЖНОЕ ДОП ШТУКА: если хочется как-то форматировать отправляемый текст, \
    # то следующим аргументом в send_message можно сделать parse_mode='html' и\
    # после писать тест в виде html код, к примеру "<b>Привет<\b>"
    # то есть мы регистриурем, какая функция будет срабатывать после выбора кнопки; аргументы - (message, название_функции)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "Пользователь":
        usefull_urls(message)
    else:
        bot.send_message(message.chat.id, "Пока не знаю, что с вами делать :(")
    remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо за выбор!", reply_markup=remove)


@bot.message_handler(commands=['usefull_urls'])
def usefull_urls(message):
    # это контейнер для будущих кнопок под сообщениями бота(есть и второй тип кнопок, не под сообщениями)
    markup = types.InlineKeyboardMarkup()
    # про дизайн кнопок: будем в отдельную переменную писать создание кнопок,
    # а markup.row(args) добавлять как раз кнопки; если мы хотим в один ряд одну кнопку,в другой ряд еще две другие, то нужно пистаь так
    # добавляем в контейнер кнопку; пишем обхяснение кнопки и саму ссылку, к примеру
    btn1 = types.InlineKeyboardButton(
        "Перейти на вики ВШЭ", url='http://wiki.cs.hse.ru/Заглавная_страница')
    btn2 = types.InlineKeyboardButton("Узнать свою оценку по ДЗ Дискры",
                                      url="https://docs.google.com/spreadsheets/d/1bfa-SilQvN_j1BF2CJG2fl5Ei2yX693b/edit?usp=sharing&ouid=107086670525368017252&rtpof=true&sd=true")
    # markup.add(btn1) черзе add на одну строку попадает одна кнопка
    # markup.row(btn1, btn2)
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(
        message.chat.id, "Выбери полезную ссылку для себя:", reply_markup=markup)
    # можно было bot.reply_to(), но, вероятно, пользовательно не будет
    # присылать что-то, а просто нажмет на команду


# чтобы файл постоянно работал(соотвественно и бот);
bot.infinity_polling()
# или можно использовать bot.infinity_polling() работает аналогично(хотя\
# документацию не читала)
# \с сайта по документации бибилотеки: Эта функция создаёт новый Thread, \
# который вызывает служебную функцию __retrieve_updates. Это позволяет боту \
# получать апдейты (Update) автоматически и вызывать соответствующие \
# листенеры и хендлеры.


# ВОЗМОЖНО ПОНАДОБИТСЯ ДЛЯЯ ПРОЕКТА
#
# import webbrowser чтобы, к примеру, при обработке какой-то команды\
# открывать сайт НО ЭТО ПЛОХОЙ СПОСОБ ПОТОМУ ЧТО ОТКРЫВАЕТ НА ЛОКАЛЬНОМ
# УСТРОЙСТВЕ, лучше делать кнопку для сайта, чтобы сам пользователь на нее тыкал
# @bot.message_handler(commands=['site'])
# def site(message):
#     webbrowser.open('http://wiki.cs.hse.ru/Заглавная_страница')


# ВАЖНЫЕ УРОКИ
# 3 урок понадобится, так как там объясняется, как обрабатывать callback_data
# и там же он показывает, как отправлять фото от бота
