from app.models.user import User as UserModel
from app.resources.v1.base import BasicProtectedResource
from flask_restful import reqparse


class User(BasicProtectedResource):
    get_parser = reqparse.RequestParser()

    def get(self, user_unid):
        user = UserModel.fetch_user_by_unid(user_unid)

        return {
            'user': user.serialize()
        }


class Users(BasicProtectedResource):

    def get(self):
        users = UserModel.get_all_users()
        users_serialized = [user.serialize() for user in users]

        return {
            'users': users_serialized
        }

