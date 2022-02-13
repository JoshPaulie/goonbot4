import datetime

current_year = datetime.date.today().year


def days_since(end_date: datetime.date, today_date: datetime.date) -> int:
    """Returns days until end_date from today_date. Used later to sort special events remaining in current year."""
    return (end_date - today_date).days


BIRTHDAYS = {
    "Hudson's Birthday": datetime.date(current_year, 2, 14),
    "Chris' Birthday": datetime.date(current_year, 4, 21),
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

SPECIAL_EVENTS = {**BIRTHDAYS, **HOLIDAYS}


def get_special_events_remaining(today_date: datetime.date) -> list[tuple[str, int]]:
    """
    Returns special events remaining for the current year

    Future Josh/Anyone else reading this: This might look messy but it's needed.
    Without a fresh datetime object being passed every call, the countdown is stuck at whatever day the bot happened to be restarted
    """
    special_events_remaining = {
        special_event: days_since(date, today_date) for special_event, date in SPECIAL_EVENTS.items() if days_since(date, today_date) > -1
    }
    special_events_remaining = sorted(special_events_remaining.items(), key=lambda x: x[1])
    return special_events_remaining
