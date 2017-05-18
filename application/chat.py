from flask_socketio import send, emit

from application import socket_io, active_users, message_history
from application.utils.decorators import auth_required, save_to_history
from application.utils.tokens import get_username_from_token
from application.utils.events import IncomingEvents, OutgoingEvents


@socket_io.on(IncomingEvents.AUTH)
def on_auth(json):
    token = json.get("token", None)
    if not token:
        send("Token is needed")
        return

    username = get_username_from_token(token)
    if not username:
        send("authentication error")
    else:
        active_users.add(username)
        send_global_history()
        send_private_history(username)
        notify_subscribers()


@socket_io.on(IncomingEvents.SEND_PRIVATE_MESSAGE)
@auth_required
def on_private_message(current_user, json):
    to_username = json.get("to", None)
    text = json.get("message", None)
    if not to_username or not text:
        return

    message = {"message": text, "author": current_user.username}
    receiver = active_users.get_user_by_username(to_username)
    if receiver:
        send_private_message(message, to_user=receiver)
        send_private_message(message, to_user=current_user)


@socket_io.on(IncomingEvents.SEND_GLOBAL_MESSAGE)
@auth_required
def on_global_message(current_user, json):
    text = json.get("message", None)
    if text:
        message = {"message": text, "author": current_user.username}
        send_global_message(message)


@socket_io.on(IncomingEvents.DISCONNECT)
@auth_required
def on_disconnect(current_user):
    active_users.remove_current_user()
    notify_subscribers()


@socket_io.on(IncomingEvents.CONNECT, namespace="/active-users")
@auth_required
def on_subscribe_for_active_users(current_user):
    active_username_list = [user.username for user in active_users.get_all()]
    send(active_username_list, namespace="/active-users")


@save_to_history
def send_private_message(message, to_user):
    emit(OutgoingEvents.SEND_PRIVATE_MESSAGE, message, room=to_user.sid)


@save_to_history
def send_global_message(message):
    emit(OutgoingEvents.SEND_GLOBAL_MESSAGE, message, broadcast=True)


def send_global_history():
    emit(OutgoingEvents.GLOBAL_MESSAGE_HISTORY, message_history.get_global())


def send_private_history(username):
    emit(OutgoingEvents.PRIVATE_MESSAGE_HISTORY, message_history.get_private(username))


def notify_subscribers():
    active_username_list = [user.username for user in active_users.get_all()]
    send(active_username_list, broadcast=True, namespace="/active-users")
