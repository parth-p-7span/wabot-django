import re
import requests


def verify_email(email):
    pat = "^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False


def verify_mobile(mobile):
    pat = "^\d{10}$"
    if re.match(pat, mobile):
        return True
    return False


def verify_url(url):
    try:
        if url[:4] == "http":
            url = "http://" + url
        return True if requests.get(url).status_code == 200 else False
    except:
        return False


def verify_age(age):
    try:
        return int(age) <= 90
    except:
        return False


def verify_number(data):
    try:
        return isinstance(int(data), int)
    except:
        return False


def verify_media(data):
    return isinstance(data, dict)


def verify_date(date):
    pat = "^(\d\d?)[-\/](\d\d?)[-\/](\d{4})$"
    if re.match(pat, date):
        return True
    return False
