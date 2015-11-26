from app.models.token import Token
from app.models.user import User
from app.models.user_team import UserTeam
from flask_restful import Resource, reqparse


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='The email to login with', required=True)
    parser.add_argument('password', type=str, help='The password', required=True)

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        if email is None or len(email) < 3:
            return {'status': 'false', 'message': 'Invalid email'}, 403

        authed = User.authenticate(email, password)

        if authed:
            user = User.fetch_user_by_email(email)
            user_team = UserTeam.get_team_by_user(user.unid)
            team_unid = user_team.team_unid if user_team else None
            token = Token(user.unid)
            return {'status': 'true', 'token': token.token, 'user_unid': user.unid, 'team_unid':team_unid}, 200
        else:
            return {'status': 'false', 'message': 'Incorrect login credentials'}, 403
        
