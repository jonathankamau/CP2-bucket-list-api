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

        # TODO create test users and bucket list
        # TODO get token for user
        self.token = {'Authorization': 'token ' + 'Token'}
        self.expired_token = {'Authorization': 'token ' + 'Token'}
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
