#!flask/bin/python
# -*- coding: utf-8 -*-

import os.path
from migrate.versioning import api

import config
from app import db

db.create_all()
if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
    api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database_repository')
    api.version_control(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(config.SQLALCHEMY_DATABASE_URI,config.SQLALCHEMY_MIGRATE_REPO,
                        api.version(config.SQLALCHEMY_MIGRATE_REPO))




