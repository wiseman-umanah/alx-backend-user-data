#!/usr/bin/env python3
"""Creates Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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
        session_cookies = self.session_cookie(request)
        return User.get(self.user_id_for_session_id(session_cookies))

    def destroy_session(self, request=None):
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
