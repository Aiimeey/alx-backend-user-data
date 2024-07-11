#!/usr/bin/env python3
"""module user session"""
from .base import Base


class UserSession(Base):
    """class user Session to save all session id"""

    def __init__(self, *args: list, **kwargs: dict):
        """Init class User session"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
