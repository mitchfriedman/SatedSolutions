from flask import Flask
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()
from app.resources.v1 import api
from app.database import stub


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    
    
    return app


def register_extensions(app):
    api.init_app(app)
    bcrypt.init_app(app)
    stub()

