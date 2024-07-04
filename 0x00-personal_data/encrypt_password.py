#!/usr/bin/env python3
"""Implement a hash_password function
that expects one string
argument name password and returns a salted,
hashed password, which is a byte string."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function to secure password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
