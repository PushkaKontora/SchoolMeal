from httpx import Cookies, Headers


def get_set_cookies(headers: Headers) -> Cookies:
    cookies = Cookies()
    header = headers.get("set-cookie") or ""

    for entry in header.split(", "):
        chunk = entry.split("; ")[0]
        key, value = chunk.split("=")
        cookies.set(key, value)

    return cookies
