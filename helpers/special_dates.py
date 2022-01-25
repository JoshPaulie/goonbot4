import datetime

today = datetime.date.today()
current_year = today.year


def days_since(end_date) -> int:
    return (end_date - today).days


BIRTHDAYS = {
    "Hudson's Birthday": datetime.date(current_year, 2, 14),
    "Chri's Birthday": datetime.date(current_year, 4, 21),
    "Alex's Birthday": datetime.date(current_year, 4, 15),
    "Daniel's Birthday": datetime.date(current_year, 4, 3),
    "Lex's Birthday": datetime.date(current_year, 5, 20),
    "Justin's Birthday": datetime.date(current_year, 6, 12),
    "Josh's Birthday": datetime.date(current_year, 6, 27),
    "Matt's Birthday": datetime.date(current_year, 9, 24),
    "Hobo's Birthday": datetime.date(current_year, 9, 11),
    "Conrad's Birthday": datetime.date(current_year, 10, 2),
    "Vynle's Birthday": datetime.date(current_year, 5, 9),
    # "Don't leave debug code in your main" ya ya shut up nerd 😎
    # "TEST's Birthday": datetime.date(current_year, today.month, today.day),
}
BIRTHDAYS = {goon + " 🧁": date for goon, date in BIRTHDAYS.items()}

HOLIDAYS = {
    "Valentine's Day 💕": datetime.date(current_year, 2, 14),
    "Freedom Day :us_flag:": datetime.date(current_year, 7, 6),
    "Thanksgiving 🦃": datetime.date(current_year, 11, 24),
    "Christmas 🎄": datetime.date(current_year, 12, 25),
}

special_events = {**BIRTHDAYS, **HOLIDAYS}
special_events_remaining = {
    special_event: days_since(date) for special_event, date in special_events.items() if days_since(date) > -1
}
special_events_remaining = sorted(special_events_remaining.items(), key=lambda x: x[1])
