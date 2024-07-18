#!/usr/bin/env python3
"""A basic Flask app
"""
from flask import (
    Flask, jsonify,
    request, abort,
    redirect, url_for,
    make_response)
from auth import Auth


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def start():
    """Start the webapp
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Registers a new user if it does not exist"""

    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except KeyError:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    response = {"email": email, "message": "user created"}
    return jsonify(response)


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """creates login session for user
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if AUTH.valid_login(user_email, user_pwd):
        session = AUTH.create_session(user_email)
        res = make_response(jsonify({"email": user_email, "message": "logged in"}))
        res.set_cookie('session_id', session)
        return res
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Destroys user session and logs out user
    """
    session_id = request.cookie.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('start'))
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """Gets user's profile via session ID
    """
    session_id = request.cookie.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token for User
    """
    user_email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(user_email)
        return jsonify({"email": user_email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    user_email = request.form.get("email")
    user_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        user_token = AUTH.get_reset_password_token(user_email)
        AUTH.update_password(user_token, new_password)
        return jsonify({"email": user_email,
                        "message": "Password update"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    AUTH = Auth()
    app.run(host="0.0.0.0", port="5000")
