#!/usr/bin/env python3
"""Basic Auth Class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
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
