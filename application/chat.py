from flask_socketio import emit

from application import socket_io
from application.models import User
from application.chat_users import active_users
from application.chat_history import message_history
from application.utils.decorators import auth_required, fields_required
from application.utils.tokens import get_username_from_token
from application.utils.events import IncomingEvents, OutgoingEvents


@socket_io.on(IncomingEvents.AUTH)
@fields_required(["token"])
def on_auth(token):
    username = get_username_from_token(token)
    if not username:
        emit(OutgoingEvents.ERROR, "Invalid token")
    else:
        active_users.add(username)
        send_global_history()
        send_private_history(username)
        notify_subscribers()


@socket_io.on(IncomingEvents.SEND_PRIVATE_MESSAGE)
@fields_required(["message", "to"])
@auth_required
def on_private_message(message, to):
    current_user = active_users.get_current()
    receiver = active_users.get_by_username(to) or User.query.filter_by(username=to).first()
    if receiver:
        current_user.send_private_message(message, to_user=receiver)


@socket_io.on(IncomingEvents.SEND_GLOBAL_MESSAGE)
@fields_required(["message"])
@auth_required
def on_global_message(message):
    current_user = active_users.get_current()
    current_user.send_public_message(message)


@socket_io.on(IncomingEvents.DISCONNECT)
@auth_required
def on_disconnect():
    active_users.remove_current()
    notify_subscribers()


@socket_io.on(IncomingEvents.CONNECT, namespace="/active-users")
@auth_required
def on_subscribe_for_active_users():
    active_username_list = [user.username for user in active_users.get_all()]
    emit(OutgoingEvents.UPDATE, active_username_list, namespace="/active-users")


def send_global_history():
    emit(OutgoingEvents.GLOBAL_MESSAGE_HISTORY, message_history.get_public())


def send_private_history(username):
    emit(OutgoingEvents.PRIVATE_MESSAGE_HISTORY, message_history.get_private(username))


def notify_subscribers():
    active_username_list = [user.username for user in active_users.get_all()]
    emit(OutgoingEvents.UPDATE, active_username_list, broadcast=True, namespace="/active-users")
