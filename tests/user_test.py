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
        assert User.query.filter_by(username=self.user_data["username"]).first()

    def test_should_return_token(self):
        assert "token" in self.response.json

    def test_should_return_token_with_data(self):
        assert self.response.json["token"]


class UserCreationNegativeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/users/"

    def test_should_return_400_without_password(self):
        response = self.json_post(self.uri, data={"username": "Cool!"})
        assert response.status_code == 400

    def test_should_return_400_without_username(self):
        response = self.json_post(self.uri, data={"password": "myPWD"})
        assert response.status_code == 400

    def test_should_not_create_user_without_password(self):
        self.json_post(self.uri, data={"username": "Cool!"})
        assert not User.query.all()

    def test_should_not_create_user_without_username(self):
        self.json_post(self.uri, data={"password": "myPWD"})
        assert not User.query.all()

    def test_should_not_create_users_with_same_username(self):
        self.json_post(self.uri, data={"username": "First",
                                       "password": "First"})
        response = self.json_post(self.uri, data={"username": "First",
                                                  "password": "First"})
        assert response.status_code == 400

    def test_should_not_return_token_for_users_with_same_username(self):
        self.json_post(self.uri, data={"username": "First",
                                       "password": "First"})
        response = self.json_post(self.uri, data={"username": "First",
                                                  "password": "First"})
        assert "token" not in response.json

    def test_should_not_return_token_without_password(self):
        response = self.json_post(self.uri, data={"username": "Cool!"})
        assert "token" not in response.json

    def test_should_not_return_token_without_username(self):
        response = self.json_post(self.uri, data={"password": "myPWD"})
        assert "token" not in response.json

    def test_should_return_different_tokens_for_different_users(self):
        first_response = self.json_post(self.uri, data={"username": "First",
                                                        "password": "First"})
        second_response = self.json_post(self.uri, data={"username": "Second",
                                                         "password": "Second"})
        assert first_response.json["token"] != second_response.json["token"]
