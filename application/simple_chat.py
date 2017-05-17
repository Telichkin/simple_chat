from flask_socketio import send
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from application import db, socket_io
from application.models import User


root = Blueprint("root", __name__)


@root.route("/users/", methods=["POST"])
def create_user():
    user_data = request.get_json()

    password = user_data.get("password", None)
    if not password:
        return jsonify({"error": "Password is needed"}), 400

    username = user_data.get("username", None)
    if not username:
        return jsonify({"error": "Username is needed"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User with current username already exists"}), 400

    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"token": create_access_token(identity=username)}), 201


@root.route("/auth/", methods=["POST"])
def token_auth():
    auth_data = request.get_json()

    username = auth_data.get("username", None)
    if not username:
        return jsonify({"error": "Username is needed"}), 400

    password = auth_data.get("password", None)
    if not password:
        return jsonify({"error": "Password is needed"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.is_password_valid(password):
        return jsonify({"error": "Incorrect username or password"}), 400

    return jsonify({"token": create_access_token(identity=username)}), 200


@socket_io.on("connect")
def connect_global_chat():
    send("Connected!")
