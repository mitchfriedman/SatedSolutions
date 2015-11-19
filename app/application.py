from flask import Flask
from app.resources.v1 import api


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    
    return app


def register_extensions(app):
    api.init_app(app)

