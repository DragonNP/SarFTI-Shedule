from datetime import datetime, timedelta


def get_current_week():
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())

    return monday.date().strftime('%d.%m.%Y')


def get_next_week():
    d = datetime.now()
    days_ahead = 0 - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (d + timedelta(days_ahead)).date().strftime('%d.%m.%Y')
