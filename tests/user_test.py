import json

from flask_testing import TestCase

import config
import application


class UserCreationPositiveTestCase(TestCase):
    def create_app(self):
        return application.create(config.TestingConfig)

    def setUp(self):
        application.db.create_all()
        self.uri = "/users/"
        self.user_data = {
            "username": "Telichkin",
            "password": "SuperPWD!"
        }

    def test_should_return_201_on_creation(self):
        response = self.get_create_response(data=self.user_data)
        assert response.status_code == 201

    def get_create_response(self, data):
        return self.client.post(self.uri,
                                data=json.dumps(data),
                                content_type="application/json")

    def tearDown(self):
        application.db.drop_all()
