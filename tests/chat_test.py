from tests.utils import BaseTestCase
from application import socket_io


class AuthBase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "username": "Telichkin",
            "password": "SuperPWD!"
        }
        self.socket_client = socket_io.test_client(self.app)
        self.socket_client.get_received()

    # SocketTO().test_client works incorrectly, it can't receive messages when more than 1
    # tests with it is written.
    def test_auth(self):
        response = self.json_post("/users/", self.user_data)
        self.socket_client.emit("auth", {"token": response.json["token"]})
        assert self.socket_client.get_received()[0]["args"] == "authenticated"

        self.socket_client.emit("auth", {"token": response.json["token"][:-3] + "qwe"})
        assert self.socket_client.get_received()[0]["args"] == "authentication error"

        self.socket_client.emit("auth", {})
        assert self.socket_client.get_received()[0]["args"] == "Token is needed"
