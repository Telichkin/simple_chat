from flask_testing import TestCase

import config
import application


class BaseTestCase(TestCase):
    def create_app(self):
        return application.create(config.TestingConfig)

    def setUp(self):
        application.db.create_all()

    def tearDown(self):
        application.db.session.remove()
        application.db.drop_all()
