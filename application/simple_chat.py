from flask_socketio import send, emit
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, tokens
from flask_jwt_extended.config import config
from jwt.exceptions import DecodeError

from application import db, socket_io, active_users
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


subscribers = set()


@socket_io.on("auth")
def auth_chat(json):
    if "token" not in json:
        send("Token is needed")
        return

    username = get_username_from_token(json["token"])
    if not username:
        send("authentication error")
    else:
        active_users.add(username)
        send("authenticated")
        notify_subscribers()


@socket_io.on("send message")
def send_message(json):
    sender = active_users.get_current_user()
    if not sender:
        return

    to_username = json.get("to", None)
    text = json.get("message", None)
    if not to_username or not text:
        return

    message = {"message": text, "author": sender.username}
    if to_username == "all":
        emit("send message", message, broadcast=True)
    else:
        receiver = active_users.get_user_by_username(to_username)
        if receiver:
            emit("send message", message, room=receiver.sid)
            emit("send message", message, room=sender.sid)


@socket_io.on("subscribe active users")
def subscribe_for_active_users():
    subscriber = active_users.get_current_user()
    if not subscriber:
        return

    subscribers.add(subscriber)
    active_username_list = [user.username for user in active_users.get_all()]
    emit("active users", active_username_list)


@socket_io.on("disconnect")
def disconnect():
    active_user = active_users.get_current_user()
    if not active_users:
        return

    if active_user in subscribers:
        subscribers.remove(active_user)

    active_users.remove_current_user()
    notify_subscribers()


def notify_subscribers():
    active_username_list = [user.username for user in active_users.get_all()]
    for subscriber in subscribers:
        emit("active users", active_username_list, room=subscriber.sid)
