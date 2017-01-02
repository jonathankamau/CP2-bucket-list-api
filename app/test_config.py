import unittest

import config
from app import db, app
from app.mod_auth.models import User
from app.mod_bucketlists.models import BucketList, BucketListItem


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client(use_cookies=False)

        config.SQLALCHEMY_DATABASE_URI = 'sqlite://'
        app.config.from_object(config)
        db.create_all()

        # test users
        self.brian = User('brian', 'password')
        self.brian.save()
        self.brian.refresh_from_db()

        self.shem = User('shem', 'password')
        self.shem.save()
        self.shem.refresh_from_db()

        # test bucket lists for each user
        self.brian_bucketlist = BucketList("Checkpoint", self.brian.id)
        self.brian_bucketlist.save()
        self.brian_bucketlist.refresh_from_db()

        self.shem_bucketlist = BucketList("Checkpoint", self.shem.id)
        self.shem_bucketlist.save()
        self.shem_bucketlist.refresh_from_db()

        # add item  to bucket list
        self.brian_bucketlist_item = BucketListItem("Write Tests", "completes checkpoint 2", self.brian_bucketlist.id)
        self.brian_bucketlist_item.save()
        self.brian_bucketlist_item.refresh_from_db()

        db.session.commit()

        # TODO get token for brian
        self.token = {'Authorization': 'token ' + 'Token'}
        self.expired_token = {'Authorization': 'token ' + 'Token'}
        self.invalid_token = {'Authorization': 'token ' + 'abc'}
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
