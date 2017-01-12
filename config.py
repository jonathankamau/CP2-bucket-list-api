import os

SECRET_KEY = '9111(enh=$kn$)5gb%88my9x925jqtp7_1ccanu%92s3_hj4o%'

DEBUG = True


SERVER_NAME = 'localhost:5000'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bucketlist.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 3
