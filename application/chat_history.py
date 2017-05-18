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


message_history = MessageHistory()
