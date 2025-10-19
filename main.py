import telebot
from telebot import types
from config import BOT_TOKEN
from keyboards import useful_urls_keyboards, role_keyboard
from db import get_random_prediction

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):  # ПЕРЕДЕЛАТЬ
    bot.send_message(
        message.chat.id, "<b>Привет</b>! Выбери, кем ты являешься для этого бота:", parse_mode='html', reply_markup=role_keyboard())


@bot.message_handler(func=lambda m: m.text == "Пользователь")
def user_student(message):
    remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо за выбор!", reply_markup=remove)
    bot.send_message(message.chat.id, "Выбери полезную ссылку:",
                     reply_markup=useful_urls_keyboards())


@bot.message_handler(func=lambda m: m.text == "Админ")
def user_admin(message):
    remove = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо за выбор!", reply_markup=remove)
    bot.send_message(message.chat.id, "Пока не знаю, что с вами делать :(")


@bot.message_handler(commands=['useful_urls'])
def useful_urls(message):
    bot.send_message(
        message.chat.id, "Выбери полезную ссылку для себя:", reply_markup=useful_urls_keyboards())


@bot.message_handler(func=lambda m: m.text == "cookie")
def send_cookie(message):
    bot.send_message(
        message.chat.id, f"Сегодня ваша печенька говорит:{get_random_prediction()}")


@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong!")


bot.infinity_polling()
