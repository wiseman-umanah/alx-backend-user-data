#!/usr/bin/env python3
"""Handle Basic Authentication
for Users
"""
from flask import request
from typing import List, TypeVar


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
            excluded_paths = [x if x.endswith("/") else x + "/"
                              for x in excluded_paths]
            if path in excluded_paths and path == "/api/v1/status/":
                return False
            if path in excluded_paths:
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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user

        Args:
            request (_type_, optional):the request. Defaults to None.

        Returns:
            TypeVar: returns None
        """
        return None
