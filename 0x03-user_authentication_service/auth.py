#!/usr/bin/env python3
"""Bcrypt password hashing
"""
import bcrypt


def _hash_password(password: str) -> bcrypt.hashpw:
    """password hashing with bcrypt

    Args:
        password (str): the password

    Returns:
        bcrypt.hashpw: _description_
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
