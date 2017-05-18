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


class MessageHistory:
    def __init__(self):
        self._global = []
        self._private = {}

    def add_global(self, message):
        self._global.append(message)

    def get_global(self):
        return self._global

    def add_private(self, message, to_username):
        if to_username not in self._private:
            self._private[to_username] = []
        self._private[to_username].append(message)

    def get_private(self, username):
        return self._private.get(username, [])

