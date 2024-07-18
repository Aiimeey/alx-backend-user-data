#!/usr/bin/env python3
"""
Create module basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def hello() -> str:
    """say welcome to the root path"""
    return jsonify({'message': 'Bienvenue'}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """create a user with post methods"""
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email and password:
        try:
            AUTH.register_user(email, password)
        except ValueError:
            return jsonify({'message': 'email already registered'}), 400
        return jsonify({'email': email, 'message': 'user created'}), 200
    return jsonify({'message': 'should have email and password'})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def session():
    """create session post module"""
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email and password and AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({'email': email, 'message': 'logged in'})
            response.set_cookie('session_id', session_id)
            return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session"""
    session_id = request.cookies.get('session_id', None)
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """get profile based on session id"""
    session_id = request.cookies.get('session_id', None)
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({'email': user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def genTokenTo_reset_password():
    """Reset password"""
    email = request.form.get('email', None)
    if email:
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": token}), 200
        except ValueError:
            pass
    abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """reset password"""
    email = request.form.get('email', None)
    reset_token = request.form.get('reset_token', None)
    new_password = request.form.get('new_password', None)
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify(
                {'email': email, 'message': 'Password updated'}
            ), 200
        except ValueError:
            pass
    abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
