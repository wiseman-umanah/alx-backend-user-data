#!/usr/bin/env python3
"""Handle Basic Authentication
for Users
"""
from flask import request
from fnmatch import fnmatch
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication

        Args:
            path (str): url
            excluded_paths (List[str]): excluded url

        Returns:
            bool: returns False or True
        """
        if path is not None and excluded_paths is not None:
            if not path.endswith("/"):
                path += '/'
            for pat in excluded_paths:
                if not pat.endswith("*"):
                    pat += "*"
                if fnmatch(path, pat):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorize header

        Args:
            request (_type_, optional):the request. Defaults to None.

        Returns:
            str: returns None
        """
        if request is not None:
            return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user

        Args:
            request (_type_, optional):the request. Defaults to None.

        Returns:
            TypeVar: returns None
        """
        return None

    def session_cookie(self, request=None):
        """Return a cookie value from a request
        """
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookies.get(session_name)
        return None
