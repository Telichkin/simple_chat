from flask import request


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
        username = self._sid_to_user[request.sid]
        del self._sid_to_user[request.sid]
        del self._username_to_user[username]

    def get_current_user(self):
        return self._sid_to_user.get(request.sid, None)

    def get_user_by_username(self, username):
        return self._username_to_user.get(username, None)
