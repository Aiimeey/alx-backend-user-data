#!/usr/bin/env python3
"""authentication module"""
from db import DB
from bcrypt import hashpw, gensalt, checkpw
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """methods that hashed password"""
    return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """generate uuid based on uuid module"""
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user based on email and password"""
        try:
            self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Check Valid login"""
        try:
            user = self._db.find_user_by(email=email)
            if checkpw(password.encode(), user.hashed_password):
                return True
        except (InvalidRequestError, NoResultFound):
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create session id using uuid"""
        try:
            user = self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user based on session id"""
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except Exception:
                pass
        return None

    def destroy_session(self, user_id: str) -> None:
        """destroy session based on user id"""
        if not user_id:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """generate token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        self._db.update_user(user.id, reset_token=_generate_uuid())
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        self._db.update_user(
            user.id,
            hashed_password=_hash_password(password),
            reset_token=None
        )
