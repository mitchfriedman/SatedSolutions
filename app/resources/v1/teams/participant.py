from app.models.user_type import UserTeam
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource


class Participants(BasicProtectedResource):
    create_parser = reqparse.RequestParser()

