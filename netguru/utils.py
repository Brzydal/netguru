import uuid
import secrets
import string


def create_hash():
    """This function generate 32 character long hash"""
    some_hash = uuid.uuid1()
    return some_hash.hex


def create_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password
