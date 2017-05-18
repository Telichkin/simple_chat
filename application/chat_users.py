from flask import request
from flask_socketio import emit

from application import redis
from application.chat_history import message_history
from application.utils.events import OutgoingEvents


class ActiveUser:
    def __init__(self, username, sid):
        self.username = str(username, "utf-8") if isinstance(username, bytes) else username
        self.sid = str(sid, "utf-8") if isinstance(sid, bytes) else sid

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
        self._storage = redis
        self._username_to_sid = "username"
        self._sid_to_username = "sid"

    def add(self, username):
        self._storage.hset(self._username_to_sid, username, request.sid)
        self._storage.hset(self._sid_to_username, request.sid, username)

    def remove_current(self):
        username = self._storage.hget(self._sid_to_username, request.sid)
        self._storage.hdel(self._sid_to_username, request.sid)
        self._storage.hdel(self._username_to_sid, username)

    def get_all(self):
        return [ActiveUser(username, sid) for username, sid
                in self._storage.hgetall(self._username_to_sid).items()]

    def get_current(self):
        username = self._storage.hget(self._sid_to_username, request.sid)
        if not username:
            return None
        return ActiveUser(username, request.sid)

    def get_by_username(self, username):
        sid = self._storage.hget(self._username_to_sid, username)
        if not sid:
            return None
        return ActiveUser(username, sid)


active_users = ActiveUsers()
