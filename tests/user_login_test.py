from application import db
from .utils import BaseTestCase
from application.models import User


class UserLoginPositive(BaseTestCase):
    def setUp(self):
        super().setUp()
        uri = "/auth/"
        username = "Test"
        password = "Test"
        user = User(username=username,
                    password=password)
        db.session.add(user)
        db.session.commit()
        self.response = self.json_post(uri, {"username": username,
                                             "password": password})

    def test_should_return_200(self):
        assert self.response.status_code == 200

    def test_should_contain_token_field(self):
        assert "token" in self.response.json

    def test_should_return_token(self):
        assert self.response.json["token"]


class UserLoginNegative(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/auth/"

    def test_should_return_400_without_username(self):
        response = self.json_post(self.uri, {"password": "Strong"})
        assert response.status_code == 400

    def test_should_not_contain_token_without_username(self):
        response = self.json_post(self.uri, {"password": "Strong"})
        assert "token" not in response.json

    def test_should_return_400_without_password(self):
        response = self.json_post(self.uri, {"username": "Test"})
        assert response.status_code == 400

    def test_should_not_contain_token_without_password(self):
        response = self.json_post(self.uri, {"username": "Test"})
        assert "token" not in response.json

    def test_should_return_400_if_user_not_exists(self):
        response = self.json_post(self.uri, {"username": "Test",
                                             "password": "Strong"})
        assert response.status_code == 400

    def test_should_not_contain_token_if_user_not_exists(self):
        response = self.json_post(self.uri, {"username": "Test",
                                             "password": "Strong"})
        assert "token" not in response.json

    def test_should_return_400_if_password_incorrect(self):
        username, password = "Test", "Test"
        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        response = self.json_post(self.uri, {"username": username,
                                             "password": password + "!"})
        assert response.status_code == 400

    def test_should_not_contain_token_if_password_incorrect(self):
        username, password = "Test", "Test"
        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        response = self.json_post(self.uri, {"username": username,
                                             "password": password + "!"})
        assert "token" not in response.json
