#!/usr/bin/env python3
""" """
from typing import List, TypeVar
from flask import request


class Auth:
    """ """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path_with_slash = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if path == excluded_path or path_with_slash == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ """
        return None
