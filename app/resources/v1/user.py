from app.models.user import User as UserModel
from app.models.user_team import UserTeam
from app.resources.v1.base import BasicProtectedResource
from flask_restful import reqparse


class User(BasicProtectedResource):

    def get(self, user_unid):
        user = UserModel.fetch_user_by_unid(user_unid)
        user_serialized = user.serialize()
        user_team = UserTeam.get_team_by_user(user_unid)
        
        user_serialized['team'] = user_team.team_unid if user_team else None

        return {
            'user': user_serialized
        }


class Users(BasicProtectedResource):

    def get(self):
        users = UserModel.get_all_users()
        users_serialized = [user.serialize() for user in users]

        return {
            'users': users_serialized
        }

