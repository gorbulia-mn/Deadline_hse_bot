import telebot
from config import BOT_TOKEN
from keyboards import useful_urls_keyboards, all_button_for_user, all_buttons_for_admin, homework_buttons
from db import get_random_prediction
from config import ADMINS
from db import init_exam, add_exam, list_future_exams, set_user_flag, list_users_flag, init_users, add_user, init_hw, add_hw, list_future_hw, set_flag_completed
from formatting import format_exams_list, format_exam_reminder, split_text_hw
from formatting import split_text_exam
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler


bot = telebot.TeleBot(BOT_TOKEN)
scheduler = BackgroundScheduler()
scheduler.start()


@bot.message_handler(commands=['start'])
def main(message):  # ПЕРЕДЕЛАТЬ
    if message.from_user.id in ADMINS:
        bot.send_message(
            message.chat.id, "Привет! Ты админ.", reply_markup=all_buttons_for_admin())
    else:
        init_users()
        add_user(message.chat.id)
        bot.send_message(
            message.chat.id, "Привет! Ты пользователь.", reply_markup=all_button_for_user())


@bot.message_handler(func=lambda m: m.text == 'Активировать напоминания')
def enable_reminders(message):
    add_user(message.chat.id)
    set_user_flag(message.chat.id, 1)
    bot.send_message(message.chat.id, 'Готово! Напоминания включены!')


@bot.message_handler(func=lambda m: m.text == 'Отключить напоминания')
def disable_reminders(message):
    add_user(message.chat.id)
    set_user_flag(message.chat.id, 0)
    bot.send_message(message.chat.id, 'Ок! Напоминания выключены')


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


@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong pong!")


@bot.message_handler(func=lambda m: m.text == 'Ближайшие экзы')
def handle_nearest_exams(message):
    exams = list_future_exams()
    text = format_exams_list(exams)
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == 'Добавить экз')
def admin_add_exam(message):
    init_exam()
    bot.send_message(
        message.chat.id, "Напиши экзамен в виде строки:\n\n<i>[курс] [тип_экза] [дд.мм.гггг] [чч:мм]</i>", parse_mode="HTML")
    bot.register_next_step_handler(message, exam_str)


def exam_str(message):
    try:
        course, exam_type, at = split_text_exam(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Возможно, ты записал экзамен не по формату. Попробуй еще раз.",
                         reply_markup=all_buttons_for_admin())
    else:
        add_exam(at=at, course=course, exam_type=exam_type)
        schedule_exam_reminders_for_all(course, exam_type, at)
        bot.send_message(message.chat.id, "Твой экзамен записан!")


def notify_exam_all(course: str, exam_type: str, at: dt.datetime, time_left_label: str):
    text = format_exam_reminder(course, exam_type, at, time_left_label)
    for chat_id in list_users_flag():
        try:
            bot.send_message(chat_id, text, parse_mode='HTML')
        except Exception:
            pass


def schedule_exam_reminders_for_all(course: str, exam_type: str, at: dt.datetime):
    now = dt.datetime.now()
    items = [("7 дней", dt.timedelta(days=7)), ("3 дня",
                                                dt.timedelta(days=3)), ("3 часа", dt.timedelta(hours=3))]
    for label, delta in items:
        run_at = at - delta
        if run_at > now:
            scheduler.add_job(notify_exam_all, trigger="date", run_date=run_at, args=(
                course, exam_type, at, label), id=f"exam_{course}_{exam_type}_{int(at.timestamp())}_{label}", replace_existing=True)


@bot.message_handler(func=lambda m: m.text == "Добавить дедлайн")
def admin_add_hw(message):
    init_hw()
    bot.send_message(
        message.chat.id, "Напиши дедлайн в виде такой строки:\n\n<i>[название_предмета] [тип_дз(дз/идз)] [номер_дз] [дд.мм.гг] [чч:мм]</i>", parse_mode="HTML")
    bot.register_next_step_handler(message, hw_str)


def hw_str(message):
    try:
        s, t, n, d = split_text_hw(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Возможно, ты записал д/з не по формату. Попробуй еще раз.",
                         reply_markup=all_button_for_user())
    else:
        add_hw(s, t, n, d)
        bot.send_message(message.chat.id, "Твой дедлайн по д/з записан!")


# @bot.message_handler(func=lambda m: m.text == "Weekly")
# def hw_send_list(message):
#     all_next_hw = list_future_hw()
#     if len(all_next_hw) == 0:
#         bot.send_message(message.chat.id, "Так список пустой шо ты кайфуй)")
#     else:
#         m = ""
#         for one in all_next_hw:
#             m += f"{one['name_subject']} {one['type_hw'].upper()}-{one['number']} {one['time'].strftime('%d.%m.%y %H:%M')}\n"
#         bot.send_message(message.chat.id, m)


@bot.message_handler(func=lambda m: m.text == "Weekly")
def hw_send_buttons(message):
    homework = list_future_hw()
    bot.send_message(
        message.chat.id, "Отметьте выполненный дедлайн:", reply_markup=(homework_buttons(homework)))


@bot.callback_query_handler(func=lambda m: m.data.startswith("hw_done:"))
def callback_done_hw(call):
    hw_id = int(call.data.split(":", 1)[1])
    set_flag_completed(hw_id)
    bot.answer_callback_query(call.id, "Домашка отмечена выполненной!")

    homework = list_future_hw()
    bot.edit_message_text("Отметьте выполненный дедлайн:", chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=homework_buttons(homework))


if __name__ == "__main__":
    init_exam()
    init_users()
    bot.infinity_polling()
