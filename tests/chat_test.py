from .utils import BaseTestCase
from application import socket_io


class ChatGlobalNamespace(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.socket_client = socket_io.test_client(self.app)

    def test_should_receive_message_after_connect(self):
        assert len(self.socket_client.get_received()) == 1
