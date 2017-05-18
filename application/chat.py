from flask_socketio import send, emit

from application import socket_io, active_users
from application.utils.decorators import auth_required
from application.utils.tokens import get_username_from_token
from application.utils.events import IncomingEvents, OutgoingEvents


def send_private_message(message, to_user):
    emit(OutgoingEvents.SEND_PRIVATE_MESSAGE, message, room=to_user.sid)


def send_global_message(message):
    emit(OutgoingEvents.SEND_GLOBAL_MESSAGE, message, broadcast=True)


def notify_subscribers():
    active_username_list = [user.username for user in active_users.get_all()]
    send(active_username_list, broadcast=True, namespace="/active-users")


class MessageHistory:
    def __init__(self):
        self._global = []
        self._private = {}

    def add_global(self, message):
        self._global.append(message)

    def get_global(self):
        return self._global

    def add_private(self, message, to_user):
        if to_user.username not in self._private:
            self._private[to_user.username] = []
        self._private[to_user.username].append(message)

    def get_private(self, username):
        return self._private.get(username, [])


message_history = MessageHistory()


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
        emit(OutgoingEvents.GLOBAL_MESSAGE_HISTORY, message_history.get_global())
        emit(OutgoingEvents.PRIVATE_MESSAGE_HISTORY, message_history.get_private(username))
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
        message_history.add_private(message, to_user=receiver)
        message_history.add_private(message, to_user=current_user)


@socket_io.on(IncomingEvents.SEND_GLOBAL_MESSAGE)
@auth_required
def on_global_message(current_user, json):
    text = json.get("message", None)
    if text:
        message = {"message": text, "author": current_user.username}
        send_global_message(message)
        message_history.add_global(message)


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
