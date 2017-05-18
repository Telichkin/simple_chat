from flask import request
from flask_socketio import emit

from application.chat_history import message_history
from application.utils.events import OutgoingEvents


class ActiveUser:
    def __init__(self, username, sid):
        self.username = username
        self.sid = sid

    def get_full_message(self, message, to_username=None):
        return {"message": message, "author": self.username, "to": to_username}

    def send_private_message(self, message, to_user):
        full_message = self.get_full_message(message, to_user.username)
        if hasattr(to_user, "sid"):
            emit(OutgoingEvents.SEND_PRIVATE_MESSAGE, full_message, room=to_user.sid)
        emit(OutgoingEvents.SEND_PRIVATE_MESSAGE, full_message, room=self.sid)
        message_history.save_private(full_message, to_user.username, self.username)

    def send_public_message(self, message):
        full_message = self.get_full_message(message)
        emit(OutgoingEvents.SEND_GLOBAL_MESSAGE, full_message, broadcast=True)
        message_history.save_public(full_message)


class ActiveUsers:
    def __init__(self):
        self._username_to_user = {}
        self._sid_to_user = {}

    def add(self, username):
        user = ActiveUser(username, request.sid)
        self._username_to_user[user.username] = user
        self._sid_to_user[user.sid] = user

    def remove_current(self):
        user = self._sid_to_user[request.sid]
        del self._sid_to_user[request.sid]
        del self._username_to_user[user.username]

    def get_all(self):
        return self._username_to_user.values()

    def get_current(self):
        return self._sid_to_user.get(request.sid, None)

    def get_by_username(self, username):
        return self._username_to_user.get(username, None)


active_users = ActiveUsers()
