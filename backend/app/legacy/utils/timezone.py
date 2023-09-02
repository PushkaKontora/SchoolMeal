from datetime import date as datetype, datetime, time as timetype

from app import config


def now() -> datetime:
    return datetime.now(tz=config.base.timezone)


def combine(date: datetype, time: timetype) -> datetime:
    return datetime.combine(date, time, config.base.timezone)
