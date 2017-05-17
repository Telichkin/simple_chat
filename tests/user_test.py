from .utils import BaseTestCase
from application.models import User


class UserCreationPositiveTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "username": "Telichkin",
            "password": "SuperPWD!"
        }
        self.response = self.json_post("/users/", self.user_data)

    def test_should_return_201(self):
        assert self.response.status_code == 201

    def test_should_create_user_in_db(self):
        assert User.query.filter_by(username=self.user_data["username"])
