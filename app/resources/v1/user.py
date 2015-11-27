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
    
    get_users_parser = reqparse.RequestParser()

    get_users_parser.add_argument('email', type=str, help='The email to filter on', required=False, location='args')


    def get(self):
        args = self.get_users_parser.parse_args()
        email = args['email']

        print(email)
        if email:
            users = UserModel.get_list(email=email.lower())
        else:
            users = UserModel.get_all_users()

        user_teams = [UserTeam.get_team_by_user(user.unid) for user in users]
        serialized = []
        for member, user in zip(user_teams, users):
            temp = user.serialize()
            temp['team_unid'] = member.team_unid if member else None
            serialized.append(temp)

        return {
            'users': serialized
        }

