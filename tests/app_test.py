from flask_testing import TestCase

import config
import application


class AppTestCase(TestCase):
    def create_app(self):
        return application.create(config.TestingConfig)

    def test_root_should_return_200(self):
        response = self.client.get('/')
        assert response.status_code == 200
