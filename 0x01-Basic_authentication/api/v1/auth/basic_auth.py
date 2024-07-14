#!/usr/bin/env python3
""" BasicAuth module"""
from api.v1.auth.auth import Auth
from base64 import b64decode, decode
import binascii
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(
       self, decoded_base64_authorization_header: str) -> (str, str):
        """
            Return:
            The user email and password from the Base64 decoded value.
        """
        if not decoded_base64_authorization_header or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
       self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ user_object_from_credentials method """
        if user_email is None or not isinstance(user_email, str) or \
           user_pwd is None or not isinstance(user_pwd, str):
            return None

        # users = User.search({'email': user_email})
        # if not users:
        #     return None
        # found_user = users[0]
        # if found_user.is_valid_password(user_pwd):
        #     return found_user
        # return None

        try:
            users = User.search({'email': user_email})
            if len(users) and users[0].is_valid_password(user_pwd):
                return users[0]
        except Exception:
            pass
        return None
