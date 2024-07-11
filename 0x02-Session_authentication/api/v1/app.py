#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialized instance by None
auth = None

# create instance from class Auth
switch = os.getenv('AUTH_TYPE', None)
if switch:
    if switch == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif switch == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif switch == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif switch == 'session_exp_auth':
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif switch == 'session_db_auth':
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()


@app.before_request
def beforeRequest() -> str:
    """handle auth before request"""
    # print(f"\033[34m *1 {request.path}\033[0m")
    if auth is not None:
        # print(f"\033[34m *2 {request.path}\033[0m")
        if auth.require_auth(request.path, [
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/',
                '/api/v1/stat*',
                '/api/v1/auth_session/login/'
        ]):
            # print("\033[34m *3 \033[0m")
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            # if auth.authorization_header(request) is None:
            #     abort(401)
            request.current_user = auth.current_user(request)
            if request.current_user is None:
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def un_authorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
