import datetime as dt

def d(d: dt.datetime) -> str: 
    return d.strftime("%d.%m.%Y")

def t(d: dt.datetime) -> str: 
    return d.strftime("%H:%M")


def format_exams_list(exams: list[dict]) -> str:
    if not exams:
        return 'Ближайших экзаменов нет'
    lines = ['<b>Ближайшие экзамены:</b>']
    for e in exams:
        lines.append(f'• <b>{e['course']}</b> — {e['exam_type']} {d(e['at'])} {t(e['at'])}')
    return "\n".join(lines)


def format_exam_reminder(course: str, exam_type: str, at: dt.datetime, time_left: str) -> str:
    return f"Напоминание\nДо {exam_type} по <b>{course}</b> осталось {time_left}.\nДата: {d(at)}\n Время: <b>{t(at)}</b>"


def split_text_hw(text: str) -> tuple[str, str, int, dt.datetime]:
    sub, t, n_str, d_str, t_str = text.strip().split()
    n = int(n_str)
    date_time_together = f"{d_str} {t_str}"
    date_time = dt.datetime.strptime(date_time_together, "%d.%m.%y %H:%M")
    return sub, t, n, date_time


def split_text_exam(text: str) -> tuple[str, str, dt.datetime]:
    # формат: "<курс> <тип_экза> <дд.мм.гггг> <чч:мм>"
    course, exam_type, d_str, t_str = text.strip().split()
    at = dt.datetime.strptime(f"{d_str} {t_str}", "%d.%m.%Y %H:%M")
    return course, exam_type, at
