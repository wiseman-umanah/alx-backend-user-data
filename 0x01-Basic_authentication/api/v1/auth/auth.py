#!/usr/bin/env python3
"""Handle Basic Authentication
for Users
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication

        Args:
            path (str): url
            excluded_paths (List[str]): excluded url

        Returns:
            bool: returns False or True
        """
        if path is not None and excluded_paths is not None:
            if path[-1] != "/":
                path += "/"
            for pat in excluded_paths:
                if pat[-1] != "/":
                    pat += "/"
                if path == pat:
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
