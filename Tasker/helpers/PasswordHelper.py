"""
Helper for passwords and strings.
"""
import hashlib
import random
import string
import bcrypt

class PasswordHelper(object):
    @staticmethod
    def hash_password(password):
        password = hashlib.sha256(bytes(password.encode('utf-8'))).hexdigest()

        password = bytes(password, 'utf-8')
        salt = bcrypt.gensalt(rounds=10, prefix=b"2a")

        return bcrypt.hashpw(password, salt).decode("utf-8")

    @staticmethod
    def check_password(password, hashed_password):
        password = password.encode('utf-8')
        password = hashlib.sha256(password).hexdigest()
        password = password.encode('utf-8')

        hashed_password = str(hashed_password).encode('utf-8')
        return bcrypt.checkpw(password, hashed_password)