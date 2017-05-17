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
        self.user_data = {
            "username": "Telichkin",
            "password": "SuperPWD!"
        }
        self.response = self.client.post("/users/",
                                         data=json.dumps(self.user_data),
                                         content_type="application/json")

    def test_should_return_201(self):
        assert self.response.status_code == 201

    def test_should_create_user_in_db(self):
        assert User.query.filter_by(username=self.user_data["username"])

    def tearDown(self):
        application.db.session.remove()
        application.db.drop_all()
