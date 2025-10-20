import telebot
from config import BOT_TOKEN
from keyboards import useful_urls_keyboards, all_button_for_user, all_buttons_for_admin
from db import get_random_prediction, init_hw, add_hw, list_future_hw
from formatting import split_text_hw
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
        bot.send_message(message.chat.id, "Выбери, что тебе нужно",
                         reply_markup=all_button_for_user())
    else:
        bot.send_message(message.chat.id, "Зачем тебе эти кнопки для пользователя? Они у тебя и так есть...", reply_markup=all_buttons_for_admin())


@bot.message_handler(commands=['buttons_admin'])
def admin_buttons(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "Выбери, что тебе нужно",
                         reply_markup=all_buttons_for_admin())
    else:
        bot.send_message(message.chat.id, "Ата-та! Куда полез, маленький пользователь? Это не для тебя...", reply_markup=all_button_for_user())


@bot.message_handler(func=lambda m: m.text == "Добавить дедлайн")
def admin_add_hw(message):
    init_hw()
    bot.send_message(
        message.chat.id, "Напиши дедлайн в виде такой строки:\n\n<i>название_предмета тип_дз(дз/идз) номер_дз дата_дедлайна время_дедлайна<i>", parse_mode="HTML")
    bot.register_next_step_handler(message, hw_str)


def hw_str(message):
    s, t, n, d = split_text_hw(message.text)
    add_hw(s, t, n, d)
    bot.send_message(message.chat.id, "Твой дедлайн по д/з записан!")


@bot.message_handler(func=lambda m: m.text == "Weekly")
def hw_send_list(message):
    all_next_hw = list_future_hw()
    if len(all_next_hw) == 0:
        bot.send_message(message.chat.id, "Так список пустой шо ты кайфуй)")
    else:
        m = ""
        for one in all_next_hw:
            m += f"{one['name_subject']} {one['type_hw'].upper()}-{one['number']} {one['time'].strftime('%d.%m.%y %H:%M')}\n"
        bot.send_message(message.chat.id, m)


@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong!")


bot.infinity_polling()
