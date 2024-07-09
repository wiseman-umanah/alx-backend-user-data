#!/usr/bin/env python3
"""Handle Basic Authentication
for Users
"""
from flask import Flask
import requests
from typing import List, TypeVar


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication

        Args:
            path (str): url
            excluded_paths (List[str]): excluded url

        Returns:
            bool: returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """authorize header

        Args:
            request (_type_, optional):the request. Defaults to None.

        Returns:
            str: returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user

        Args:
            request (_type_, optional):the request. Defaults to None.

        Returns:
            TypeVar: returns None
        """
        return None
