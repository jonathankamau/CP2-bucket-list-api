import unittest

import config
from app import db, app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client(use_cookies=False)

        config.SQLALCHEMY_DATABASE_URI = 'sqlite://'
        app.config.from_object(config)
        db.create_all()

        # create test users and bucket list
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
