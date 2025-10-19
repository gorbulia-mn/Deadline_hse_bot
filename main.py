import telebot
from telebot import types
import sqlite3
from config import BOT_TOKEN
from keyboards import useful_urls_keyboards, role_keyboard

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):  # ПЕРЕДЕЛАТЬ
    bot.send_message(
        message.chat.id, "<b>Привет</b>! Выбери, кем ты являешься для этого бота:", parse_mode='html', reply_markup=role_keyboard())
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо за выбор!", reply_markup=remove)
    if message.text == "Пользователь":
        useful_urls(message)
    else:
        bot.send_message(message.chat.id, "Пока не знаю, что с вами делать :(")


@bot.message_handler(commands=['useful_urls'])
def useful_urls(message):
    bot.send_message(
        message.chat.id, "Выбери полезную ссылку для себя:", reply_markup=useful_urls_keyboards())


@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong!")


bot.infinity_polling()
