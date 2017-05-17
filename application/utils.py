from flask import request
from flask_jwt_extended import tokens
from flask_jwt_extended.config import config
from jwt.exceptions import DecodeError


class ActiveUser:
    def __init__(self, username, sid):
        self.username = username
        self.sid = sid


class ActiveUsers:
    def __init__(self):
        self._username_to_user = {}
        self._sid_to_user = {}

    def add(self, username):
        user = ActiveUser(username, request.sid)
        self._username_to_user[user.username] = user
        self._sid_to_user[user.sid] = user

    def remove_current_user(self):
        user = self._sid_to_user[request.sid]
        del self._sid_to_user[request.sid]
        del self._username_to_user[user.username]

    def get_all(self):
        return self._username_to_user.values()

    def get_current_user(self):
        return self._sid_to_user.get(request.sid, None)

    def get_user_by_username(self, username):
        return self._username_to_user.get(username, None)


def get_username_from_token(token):
    try:
        username = tokens.decode_jwt(token, config.decode_key, config.algorithm, csrf=False)["identity"]
    except DecodeError:
        username = None
    return username
