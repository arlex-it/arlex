"""
Helper for passwords and strings.
"""
import hashlib
import random
import string
import bcrypt


class PasswordUtilities(object):
    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode())