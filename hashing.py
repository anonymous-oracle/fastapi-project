import hashlib
from uuid import uuid4
from config import SECRET_KEY


def gen_salt():
    return hashlib.sha3_512(uuid4().bytes + SECRET_KEY).digest()


def hash_pwd(password: str, salt: bytes):
    return hashlib.sha3_512(salt + password.encode()).digest()


def check_pwd(password: str, hashed_password: bytes, salt: bytes):
    return hash_pwd(password=password, salt=salt) == hashed_password


if __name__ == "__main__":
    salt = gen_salt()
    password = "admin123"
    hashedpassword = hash_pwd(password=password, salt=salt)
    print(check_pwd(password=password, salt=salt, hashed_password=hashedpassword))
