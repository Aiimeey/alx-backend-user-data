#!/usr/bin/env python3
""" BasicAuth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class"""
    def extract_base64_authorization_header(
       self, authorization_header: str) -> str:
        """the Base64 part of the Authorization header for a Basic Auth"""
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        value = authorization_header.split(" ")
        return value[1] if len(value) > 1 else None
