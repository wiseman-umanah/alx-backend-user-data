#!/usr/bin/env python3
"""Basic Auth Class
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth Class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """function for extracting base64

        Args:
            authorization_header (str): header param

        Returns:
            str: None or authorization header
        """
        if authorization_header is not None:
            if isinstance(authorization_header, str):
                head = authorization_header.split()
                if head[0] == "Basic":
                    return " ".join(head[-1:])
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """function for decoding base64

        Args:
            authorization_header (str): header param

        Returns:
            str: None or authorization header
        """
        x = base64_authorization_header
        if x is None or not isinstance(x, str):
            return None

        try:
            decoded_bytes = base64.b64decode(x)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Validate users credentials
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
