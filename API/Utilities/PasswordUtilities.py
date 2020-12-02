"""
Helper for passwords and strings.
"""
import hashlib
import random
import string
import bcrypt
import secrets


class PasswordUtilities(object):
    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode())

    @staticmethod
    def generate_password():
        """
            generate a 20 length password with letters, digits and special characters
        """
        alphabet = string.ascii_letters + string.digits + string.printable + string.punctuation
        return ''.join(secrets.choice(alphabet) for i in range(20))
