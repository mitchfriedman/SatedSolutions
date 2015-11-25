from flask_restful import Resource
from app.auth import authenticate


class BasicProtectedResource(Resource):
    method_decorators = [authenticate]

