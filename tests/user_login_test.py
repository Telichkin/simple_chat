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
