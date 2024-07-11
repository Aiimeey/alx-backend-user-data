#!/usr/bin/env python3
"""Module class to manage the API authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """class for authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        # add allowing * of end of excluded path
        for exclude in excluded_paths:
            # print(f"\033[33m *1 {exclude} {path}\033[0m")
            if exclude[-1] != '*' or len(exclude[:-1]) > len(path):
                # print(f"\033[33m *2 {exclude} {path}\033[0m")
                continue
            exclude = exclude[:-1]
            # print(f"\033[33m *3 {exclude} {path}\033[0m")
            if exclude == path[:len(exclude)]:
                return False

        path = path if path[-1] == '/' else f'{path}/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """current user"""
        return None

    def session_cookie(self, request=None):
        """Return a cookie value from a request"""
        if request is None:
            return None
        nameCookie = getenv("SESSION_NAME", None)
        return request.cookies.get(nameCookie, None)
