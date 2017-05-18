class MessageHistory:
    def __init__(self):
        self._global = []
        self._private = {}

    def save_public(self, message):
        self._global.append(message)

    def get_public(self):
        return self._global

    def save_private(self, message, to_username, from_username):
        self._save_one_private(message, to_username)
        self._save_one_private(message, from_username)

    def _save_one_private(self, message, username):
        if username not in self._private:
            self._private[username] = []
        self._private[username].append(message)

    def get_private(self, username):
        return self._private.get(username, [])


message_history = MessageHistory()
