import hashlib
import os

from fasttower.conf import settings


def hash_password(password: str, salt: bytes = None) -> str:
    salted_password = f"{password}{settings.SECRET_KEY}".encode('utf-8')
    if salt is None:
        salt = os.urandom(16)

    hashed_password = hashlib.scrypt(salted_password, salt=salt, n=16384, r=8, p=1, dklen=64)
    return f"{salt.hex()}:{hashed_password.hex()}"


def check_password(password_check: str, password: str) -> bool:
    salt_hex, stored_hash_hex = password_check.split(':')
    salt = bytes.fromhex(salt_hex)
    hashed_password = hash_password(password, salt)
    return hashed_password.split(':')[1] == stored_hash_hex
