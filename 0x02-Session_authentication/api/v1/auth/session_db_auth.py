#!/usr/bin/env python3
"""session database authentication"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """class SessionDBAuth"""

    def create_session(self, user_id=None):
        """create new session and save session id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        data = dict(self.user_id_by_session_id[session_id])
        data['session_id'] = session_id
        data['created_at'] = data.get(
            'created_at').strftime("%Y-%m-%dT%H:%M:%S")
        user_session = UserSession(**data)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user_id from session id"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """destroy session"""
        session_id = self.session_cookie(request)
        try:
            delete_session = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(delete_session) <= 0:
            return False
        delete_session[0].remove()
        return True
