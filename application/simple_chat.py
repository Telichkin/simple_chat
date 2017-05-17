from flask_socketio import send, emit

from application import socket_io, active_users
from application.utils import get_username_from_token
from application.decorators import user_should_be_active
from application.events import IncomingEvents, OutgoingEvents


def send_message(message, to_user):
    emit(OutgoingEvents.SEND_MESSAGE, message, room=to_user.sid)


def broadcast_message(message):
    emit(OutgoingEvents.SEND_MESSAGE, message, broadcast=True)


def notify_subscribers():
    active_username_list = [user.username for user in active_users.get_all()]
    send(active_username_list, broadcast=True, namespace="/active-users")


@socket_io.on(IncomingEvents.AUTH)
def on_user_auth(json):
    token = json.get("token", None)
    if not token:
        send("Token is needed")
        return

    username = get_username_from_token(token)
    if not username:
        send("authentication error")
    else:
        active_users.add(username)
        send("authenticated")
        notify_subscribers()


@socket_io.on(IncomingEvents.SEND_MESSAGE)
@user_should_be_active
def on_send_message(current_user, json):
    to_username = json.get("to", None)
    text = json.get("message", None)
    if not to_username or not text:
        return

    message = {"message": text, "author": current_user.username}
    if to_username == "all":
        broadcast_message(message)
    else:
        receiver = active_users.get_user_by_username(to_username)
        if receiver:
            send_message(message, to_user=receiver)
            send_message(message, to_user=current_user)


@socket_io.on(IncomingEvents.DISCONNECT)
@user_should_be_active
def on_disconnect(current_user):
    active_users.remove_current_user()
    notify_subscribers()


@socket_io.on(IncomingEvents.CONNECT, namespace="/active-users")
@user_should_be_active
def on_subscribe_for_active_users(current_user):
    active_username_list = [user.username for user in active_users.get_all()]
    send(active_username_list, namespace="/active-users")
