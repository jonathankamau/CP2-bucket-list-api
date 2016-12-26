from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.mod_auth.controller import mod_auth
from app.mod_bucketlists.controller import mod_bucketlists

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

app.register_blueprint(mod_bucketlists)
app.register_blueprint(mod_auth)
