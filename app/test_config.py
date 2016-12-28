import unittest

import config
from app import db, app


class BaseTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        config.SQLALCHEMY_DATABASE_URI = 'sqlite://'
        app.config.from_object(config)
        db.create_all()

        # create test users and bucket list
        response = self.client.get('/auth/register')
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
