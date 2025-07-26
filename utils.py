import re
import string
import secrets


def random_code(length=6):
    return "".join(secrets.choice(string.digits) for _ in range(length))


def random_secret_key(length=64):
    return "".join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)
