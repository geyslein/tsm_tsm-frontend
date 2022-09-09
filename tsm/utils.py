import secrets
import string


def generate_password(length):
    chars = string.ascii_letters + string.digits
    password = ''

    for _ in range(length):
        password += secrets.choice(chars)

    return password
