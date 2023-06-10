from datetime import date as datetype, datetime, time as timetype

from app.config import TIMEZONE


def now() -> datetime:
    return datetime.now(tz=TIMEZONE)


def combine(date: datetype, time: timetype) -> datetime:
    return datetime.combine(date, time, TIMEZONE)
