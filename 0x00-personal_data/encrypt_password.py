#!/usr/bin/env python3
"""Implement a hash_password function
that expects one string
argument name password and returns a salted,
hashed password, which is a byte string."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function to secure password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function to validate passwords"""
    return bcrypt.checkpw(password.encode(), hashed_password)
