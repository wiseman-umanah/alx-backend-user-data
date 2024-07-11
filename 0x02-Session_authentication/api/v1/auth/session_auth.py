#!/usr/bin/env python3
"""Creates Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Function to create user session
        based on id
        """
        if user_id:
            if isinstance(user_id, str):
                id = str(uuid4())
                self.user_id_by_session_id[id] = user_id
                return id
