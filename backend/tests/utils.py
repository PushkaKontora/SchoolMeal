from datetime import date, datetime

from httpx import Cookies, Headers


def get_set_cookies(headers: Headers) -> Cookies:
    cookies = Cookies()
    header = headers.get("set-cookie") or ""

    for entry in header.split(", "):
        chunk = entry.split("; ")[0]
        key, value = chunk.split("=")
        cookies.set(key, value)

    return cookies


def datetime_to_str(time: datetime | None) -> str | None:
    return time.isoformat(sep="T") if time is not None else None


def date_to_str(d: date | None) -> str | None:
    return str(d) if d is not None else None


def prepare_patch_data(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}
