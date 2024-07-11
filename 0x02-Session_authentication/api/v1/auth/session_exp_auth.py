#!/usr/bin/env python3
"""handle session expiration authorization"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class Session Expiration authorization"""

    def __init__(self) -> None:
        from os import getenv
        try:
            value = int(getenv('SESSION_DURATION', '0'))
        except TypeError:
            value = 0
        # print(f"\033[33m{value}\033[0m")
        self.session_duration = value

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user_id from session_id"""
        if session_id is None or \
                self.user_id_by_session_id.get(
                session_id, None) is None:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if self.user_id_by_session_id[session_id].get(
                'created_at', None) is None:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()
        if current_time > expiration_time:
            return None
        return self.user_id_by_session_id[session_id]['user_id']
