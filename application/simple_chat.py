from flask_socketio import send, emit
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, tokens
from flask_jwt_extended.config import config
from jwt.exceptions import DecodeError

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


def get_username_from_token(token):
    try:
        username = tokens.decode_jwt(token, config.decode_key, config.algorithm, csrf=False)["identity"]
    except DecodeError:
        username = None
    return username


active_users = {}


@socket_io.on("auth")
def auth_global_chat(json):
    if "token" not in json:
        send("Token is needed")
        return

    username = get_username_from_token(json["token"])
    if not username:
        send("authentication error")
    else:
        send("authenticated")
        active_users[username] = request.sid


@socket_io.on("send message")
def send_message(json):
    if request.sid not in active_users.values():
        return

    to = json.get("to", None)
    message = json.get("message", None)
    if not to or not message:
        return

    if to == "all":
        emit("send message", {"message": message}, broadcast=True)
    else:
        private_room = active_users.get(to, None)
        if private_room:
            emit("send message", {"message": message}, room=private_room)
            emit("send message", {"message": message}, room=request.sid)
