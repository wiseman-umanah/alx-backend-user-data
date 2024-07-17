#!/usr/bin/env python3
"""Bcrypt password hashing
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bcrypt.hashpw:
    """password hashing with bcrypt

    Args:
        password (str): the password

    Returns:
        bcrypt.hashpw: _description_
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        """register new user in db
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except Exception:
            h_pwd = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=h_pwd)
