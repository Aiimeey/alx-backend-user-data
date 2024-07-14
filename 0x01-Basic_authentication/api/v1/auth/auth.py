#!/usr/bin/env python3
""" Auth module"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path_with_slash = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path or path_with_slash == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header method """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method"""
        return None
