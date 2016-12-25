from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from app.mod_index.controller import mod_index

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

#app.register_blueprint(mod_index)
