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
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the User id based on the Session id
        """
        if session_id:
            if isinstance(session_id, str):
                return self.user_id_by_session_id.get(session_id, None)
        return None

    def current_user(self, request=None):
        """Returns a User instance based on the request
        """
        