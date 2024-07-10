#!/usr/bin/env python3
"""Basic Auth Class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is not None:
            if isinstance(authorization_header, str):
                head = authorization_header.split()
                if head[0] == "Basic":
                    return " ".join(head[-1:])
        return None
