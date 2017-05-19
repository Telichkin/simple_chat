class IncomingEvents:
    AUTH = "auth"
    SEND_PRIVATE_MESSAGE = "send private message"
    SEND_GLOBAL_MESSAGE = "broadcast"
    CONNECT = "connect"
    DISCONNECT = "disconnect"


class OutgoingEvents:
    SEND_PRIVATE_MESSAGE = "send private message"
    SEND_GLOBAL_MESSAGE = "broadcast"
    PRIVATE_MESSAGE_HISTORY = "private history"
    GLOBAL_MESSAGE_HISTORY = "broadcast history"
    ERROR = "error"
    UPDATE = "update"
