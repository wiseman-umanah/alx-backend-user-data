#!/usr/bin/env python3
"""Handles all Session ROutes
"""
from flask import jsonify, abort
from api.v1.views import app_views
from flask import request
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user():
    """Login users
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not (email):
        return jsonify({ "error": "email missing" }), 404
    if not (password):
        return jsonify({ "error": "password missing" }), 404
    users = User.search({'email': email})
    if len(users) <= 0:
        return jsonify({ "error": "no user found for this email" }), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(getenv("SESSION_NAME"), sessiond_id)
        return res
    return jsonify({"error": "wrong password"}), 401
