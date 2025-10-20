import telebot
from telebot import types
from config import BOT_TOKEN
from keyboards import useful_urls_keyboards, role_keyboard, all_button_for_user, all_buttons_for_admin
from db import get_random_prediction, init_hw, add_hw
from config import ADMINS

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):  # ПЕРЕДЕЛАТЬ
    if message.from_user.id in ADMINS:
        bot.send_message(
            message.chat.id, "Привет! Ты админ.", reply_markup=all_buttons_for_admin())
    else:
        bot.send_message(
            message.chat.id, "Привет! Ты пользователь.", reply_markup=all_button_for_user())


@bot.message_handler(commands=['useful_urls'])
def useful_urls(message):
    bot.send_message(
        message.chat.id, "Выберите полезную ссылку:", reply_markup=useful_urls_keyboards())


@bot.message_handler(func=lambda m: m.text == "Печенька!")
def send_cookie(message):
    bot.send_message(
        message.chat.id, get_random_prediction())


@bot.message_handler(commands=['buttons_user'])
def user_buttons(message):
    if message.from_user.id not in ADMINS:
        bot.send_message(message.chat.id, "Выберите, что вам нужно",
                         reply_markup=all_button_for_user())


@bot.message_handler(commands=['buttons_admin'])
def admin_buttons(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "Выберите, что вам нужно",
                         reply_markup=all_buttons_for_admin())


@bot.message_handler(func=lambda m: m.text == "Добавить дедлайн")
def admin_add_hw(message):
    init_hw()
    bot.send_message(
        message.chat.id, "Напиши дедлайн в виде такой строки:\n название_предмета тип_дз(дз/идз) номер_дз дата_дедлайна время_дедлайна")
    bot.register_next_step_handler(message, hw_str)


def hw_str(message):
    line = message.text.strip()
    add_hw(line[0], line[1], line[2], line[3])
    bot.send_message(message.chat.id, "Что-то получилось?")


@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong!")


bot.infinity_polling()
