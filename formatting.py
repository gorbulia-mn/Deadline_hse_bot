import datetime as dt


def split_text_hw(text: str) -> tuple[str, str, int, dt.datetime]:
    sub, t, n_str, d_str, t_str = text.strip().split()
    n = int(n_str)
    date_time_together = f"{d_str} {t_str}"
    date_time = dt.datetime.strptime(date_time_together, "%d.%m.%y %H:%M")
    return sub, t, n, date_time
