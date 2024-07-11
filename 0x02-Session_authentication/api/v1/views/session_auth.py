#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login session"""
    from api.v1.app import auth
    from os import getenv
    email = request.form.get('email', '')
    if len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password', '')
    if len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not len(user):
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    # print(f"\033[32m{getenv('SESSION_NAME')}:{session_id}\033[0m")
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
