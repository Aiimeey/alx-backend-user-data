#!/usr/bin/env python3
""" BasicAuth module"""
from api.v1.auth.auth import Auth
from base64 import b64decode, decode
import binascii


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

    def decode_base64_authorization_header(
       self, base64_authorization_header: str) -> str:
        """Return:
            The decoded value of a Base64 string
        """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            data_bytes = b64decode(base64_authorization_header, validate=True)
            return data_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None
