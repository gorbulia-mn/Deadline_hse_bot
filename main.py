import telebot
from telebot import types
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):  # ПЕРЕДЕЛАТЬ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пользователь")
    btn2 = types.KeyboardButton("Админ")
    markup.row(btn1, btn2)
    bot.send_message(
        message.chat.id, "<b>Привет</b>! Выбери, кем ты являешься для этого бота:", parse_mode='html', reply_markup=markup)
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
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        "Перейти на вики ВШЭ", url='http://wiki.cs.hse.ru/Заглавная_страница')
    btn2 = types.InlineKeyboardButton("Узнать свою оценку по ДЗ Дискры",
                                      url="https://docs.google.com/spreadsheets/d/1bfa-SilQvN_j1BF2CJG2fl5Ei2yX693b/edit?usp=sharing&ouid=107086670525368017252&rtpof=true&sd=true")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(
        message.chat.id, "Выбери полезную ссылку для себя:", reply_markup=markup)


bot.infinity_polling()
