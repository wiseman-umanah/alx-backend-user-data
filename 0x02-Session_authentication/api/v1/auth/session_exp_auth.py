#!/usr/bin/env python3
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expire class
    """
    def __init__(self):
        self.session_duration = int(getenv("SESSION_DURATION"))
        if not self.session_duration:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """creates a session expiration
        """
        sessionId = super().create_session(user_id)
        if not sessionId:
            return None
        self.user_id_by_session_id[sessionId] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return sessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Check user session
        """
        if not session_id:
            return None
        user_det = self.user_id_by_session_id.get(session_id, None)
        if not user_det:
            return None
        if self.session_duration <= 0:
            return None
        created_at = user_det.get("created_at", None)
        if not created_at:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return user_det.get("user_id")
