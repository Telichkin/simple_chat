from flask_socketio import send, emit
from flask_jwt_extended import tokens
from flask_jwt_extended.config import config
from jwt.exceptions import DecodeError

from application import socket_io, active_users


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
