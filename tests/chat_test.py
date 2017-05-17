from tests.utils import BaseTestCase
from application import socket_io


class AuthBase(BaseTestCase):
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
    def test_auth(self):
        self.client_list[0] = socket_io.test_client(self.app)
        self.client_list[0].get_received()

        self.client_list[0].emit("auth", {"token": self.token_list[0]})
        assert self.client_list[0].get_received()[0]["args"] == "authenticated"

        self.client_list[0].emit("auth", {"token": self.token_list[0][:-3] + "qwe"})
        assert self.client_list[0].get_received()[0]["args"] == "authentication error"

        self.client_list[0].emit("auth", {})
        assert self.client_list[0].get_received()[0]["args"] == "Token is needed"

        # Not auth broadcasting
        self.client_list[1].emit("send message", {"to": "all", "message": self.message})
        response_list = [client.get_received() for client in self.client_list]
        assert all([len(response) == 0 for response in response_list])

        # Auth broadcasting
        self.client_list[1].emit("auth", {"token": self.token_list[1]})
        self.client_list[2].emit("auth", {"token": self.token_list[2]})
        self.client_list[1].get_received(), self.client_list[2].get_received()

        self.client_list[0].emit("send message", {"to": "all", "message": self.message})
        response_list = [client.get_received()[0]["args"][0] for client in self.client_list]
        assert all([response["message"] == self.message for response in response_list])
        # assert all([response["author"] == self.user_data_list[0]["username"] for response in response_list])

        # Private talk
        self.client_list[0].emit("send message", {"to": self.user_data_list[1]["username"],
                                                  "message": self.message})
        response_list = [client.get_received()[0]["args"][0] for client in self.client_list[:2]]
        assert all([response["message"] == self.message for response in response_list])
