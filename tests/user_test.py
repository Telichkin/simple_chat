from flask_testing import TestCase

import config
import application


class UserCreationPositiveTestCase(TestCase):
    def create_app(self):
        return application.create(config.TestingConfig)

    def setUp(self):
        self.uri = "/users/"
        self.user_data = {
            "username": "Telichkin",
            "password": "SuperPWD!"
        }

    def test_should_return_201_on_creation(self):
        response = self.client.post(self.uri, data=self.user_data)
        assert response.status_code == 201
