from application import db
from .utils import BaseTestCase
from application.models import User


class UserLoginPositive(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/auth/"
        self.username = "Test"
        self.password = "Test"
        user = User(username=self.username,
                    password=self.password)
        db.session.add(user)
        db.session.commit()

    def test_should_return_200(self):
        response = self.json_post(self.uri, {"username": self.username,
                                             "password": self.password})
        assert response.status_code == 200
