import json

from flask_testing import TestCase

import config
import application
from application.models import User


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

    def test_should_return_201(self):
        response = self.get_create_response(data=self.user_data)
        assert response.status_code == 201

    def test_should_create_user_in_db(self):
        self.get_create_response(data=self.user_data)
        assert User.query.filter_by(username=self.user_data["username"])

    def get_create_response(self, data):
        return self.client.post(self.uri,
                                data=json.dumps(data),
                                content_type="application/json")

    def tearDown(self):
        application.db.session.remove()
        application.db.drop_all()
