#!/usr/bin/env python3
"""Bcrypt password hashing
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """password hashing with bcrypt

    Args:
        password (str): the password

    Returns:
        bcrypt.hashpw: _description_
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates a new uuid

    Returns:
        str: return a uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register new user in db
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            h_pwd = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=h_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Creates new user session
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user_session = _generate_uuid()
                self._db.update_user(user.id, session_id=user_session)
                return user_session
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """Finds user object based on the session_id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session
        """
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """password reset function of user
        """
        try:
            user = self._db.find_user_by(email=email)
            token = str(uuid4())
            self._db.update_user(user.id, reset_token=token)
            return user.reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update User's password based on reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=password)
            return None
        except Exception:
            raise ValueError
