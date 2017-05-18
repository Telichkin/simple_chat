import json

from application import redis


class MessageHistory:
    def __init__(self):
        self._storage = redis
        self._public = "public messages"
        self._private = "private messages"

    def save_public(self, message):
        self._storage.sadd(self._public, json.dumps(message))

    def get_public(self):
        return [json.loads(message) for message in
                self._storage.smembers(self._public)]

    def save_private(self, message, to_username, from_username):
        self._storage.sadd(self._get_private_namespace(to_username), json.dumps(message))
        self._storage.sadd(self._get_private_namespace(from_username), json.dumps(message))

    def get_private(self, username):
        return [json.loads(message) for message in
                self._storage.smembers(self._get_private_namespace(username))]

    def _get_private_namespace(self, username):
        return f"{self._private}:{username}"


message_history = MessageHistory()
