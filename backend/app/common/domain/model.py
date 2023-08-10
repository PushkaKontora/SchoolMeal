from datetime import datetime

from app import config


def now() -> datetime:
    return datetime.now(config.datetime.timezone)
