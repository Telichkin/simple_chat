class IncomingEvents:
    AUTH = "auth"
    SEND_PRIVATE_MESSAGE = "send private message"
    SEND_GLOBAL_MESSAGE = "broadcast"
    CONNECT = "connect"
    DISCONNECT = "disconnect"


class OutgoingEvents:
    SEND_MESSAGE = "send message"
