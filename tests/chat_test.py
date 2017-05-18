from application import socket_io
from application.utils.events import IncomingEvents, OutgoingEvents
from tests.utils import BaseTestCase


class SocketIOTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data_list = [
            {"username": "Telichkin", "password": "SuperPWD!"},
            {"username": "Some", "password": "Other"},
            {"username": "John", "password": "Doe"}
        ]
        self.client_list = [socket_io.test_client(self.app) for _ in self.user_data_list]
        self.token_list = [self.json_post("/users/", user_data).json["token"]
                           for user_data in self.user_data_list]
        self.message = "What's up?!"

    # SocketTO().test_client works incorrectly, it can't receive messages when more than 1
    # tests with it is written.
    def test_all_socket_functionality(self):
        self.client_list[0] = socket_io.test_client(self.app)
        self.client_list[0].get_received()

        # Get message list after auth
        self.client_list[0].emit(IncomingEvents.AUTH, {"token": self.token_list[0]})
        assert self.client_list[0].get_received()[0]["args"][0] == []

        # Not auth with incorrect token
        self.client_list[0].emit(IncomingEvents.AUTH, {"token": self.token_list[0][:-3] + "qwe"})
        assert self.client_list[0].get_received()[0]["args"] == "Invalid token"

        # Not auth without token
        self.client_list[0].emit(IncomingEvents.AUTH, {})
        assert self.client_list[0].get_received()[0]["args"] == "Missed required fields: ['token']"

        # Not broadcasting without auth
        self.client_list[1].emit(IncomingEvents.SEND_GLOBAL_MESSAGE, {"message": self.message})
        response_list = [client.get_received() for client in self.client_list]
        assert all([len(response) == 0 for response in response_list])

        # Broadcasting with auth
        self.client_list[1].emit(IncomingEvents.AUTH, {"token": self.token_list[1]})
        self.client_list[2].emit(IncomingEvents.AUTH, {"token": self.token_list[2]})
        self.client_list[1].get_received(), self.client_list[2].get_received()

        self.client_list[0].emit(IncomingEvents.SEND_GLOBAL_MESSAGE, {"message": self.message})
        response_list = [client.get_received()[0]["args"][0] for client in self.client_list]
        assert all([response["message"] == self.message for response in response_list])
        assert all([response["author"] == self.user_data_list[0]["username"] for response in response_list])
        assert all([response["to"] is None for response in response_list])

        # Private talk
        self.client_list[0].emit(IncomingEvents.SEND_PRIVATE_MESSAGE, {"to": self.user_data_list[1]["username"],
                                                                       "message": self.message})
        response_list = [client.get_received()[0]["args"][0] for client in self.client_list[:2]]
        assert all([response["message"] == self.message for response in response_list])
        assert all([response["author"] == self.user_data_list[0]["username"] for response in response_list])
        assert all([response["to"] == self.user_data_list[1]["username"] for response in response_list])

        # Get all active users
        self.client_list[1].connect(namespace="/active-users")
        response = self.client_list[1].get_received("/active-users")[0]["args"]
        assert sorted(response) == sorted([user["username"] for user in self.user_data_list])

        # Notify subscribers if someone disconnect
        self.client_list[0].disconnect()
        response = self.client_list[1].get_received("/active-users")[0]["args"]
        assert sorted(response) == sorted([user["username"] for user in self.user_data_list[1:]])

        # Notify subscribers if someone connect
        self.client_list[0].connect()
        self.client_list[0].emit(IncomingEvents.AUTH, {"token": self.token_list[0]})
        response = self.client_list[1].get_received("/active-users")[0]["args"]
        assert sorted(response) == sorted([user["username"] for user in self.user_data_list])

        # Get global message history after connect
        global_message_history = self.client_list[0].get_received()[0]["args"][0]
        assert global_message_history == [{"message": self.message, "author": self.user_data_list[0]["username"],
                                           "to": None}]

        # Get private message history after connect
        self.client_list[2].emit(IncomingEvents.SEND_PRIVATE_MESSAGE,
                                 {"message": self.message, "to": self.user_data_list[1]["username"]})
        self.client_list[1].disconnect()
        self.client_list[1].connect()
        self.client_list[1].emit(IncomingEvents.AUTH, {"token": self.token_list[1]})
        # # # User 0 sent private message earlier # # #
        expected_history = [{"message": self.message, "author": self.user_data_list[0]["username"],
                             "to": self.user_data_list[1]["username"]},
                            {"message": self.message, "author": self.user_data_list[2]["username"],
                             "to": self.user_data_list[1]["username"]}]
        actual_history = [received["args"][0] for received in self.client_list[1].get_received()
                          if received["name"] == OutgoingEvents.PRIVATE_MESSAGE_HISTORY][0]
        assert sorted(actual_history, key=lambda x: x["author"]) == \
               sorted(expected_history, key=lambda x: x["author"])

        # Get private message even user is offline
        self.client_list[0].disconnect()
        self.client_list[2].emit(IncomingEvents.SEND_PRIVATE_MESSAGE,
                                 {"message": self.message, "to": self.user_data_list[0]["username"]})
        self.client_list[1].emit(IncomingEvents.SEND_PRIVATE_MESSAGE,
                                 {"message": self.message, "to": self.user_data_list[0]["username"]})
        expected_history = [{"message": self.message, "author": self.user_data_list[0]["username"],
                             "to": self.user_data_list[1]["username"]},
                            {"message": self.message, "author": self.user_data_list[2]["username"],
                             "to": self.user_data_list[0]["username"]},
                            {"message": self.message, "author": self.user_data_list[1]["username"],
                             "to": self.user_data_list[0]["username"]}]
        self.client_list[0].connect()
        self.client_list[0].emit(IncomingEvents.AUTH, {"token": self.token_list[0]})
        actual_history = [received["args"][0] for received in self.client_list[0].get_received()
                          if received["name"] == OutgoingEvents.PRIVATE_MESSAGE_HISTORY][0]
        assert sorted(actual_history, key=lambda x: x["author"]) ==\
            sorted(expected_history, key=lambda x: x["author"])
