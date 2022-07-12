import re


def verify_email(email):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False


def verify_mobile(mobile):
    pat = "^\d{10}$"
    if re.match(pat, mobile):
        return True
    return False


def verify_url(url):
    pat = ""
    if re.match(pat, url):
        return True
    return False

print(verify_url("https://google.com"))