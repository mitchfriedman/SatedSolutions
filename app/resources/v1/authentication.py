from app.models.token import Token
from app.models.user import User
from flask_restful import Resource, reqparse


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='The email to login with', required=True)
    parser.add_argument('password', type=str, help='The password', required=True)

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        authed = User.authenticate(email, password)
        if authed:
            user = User.fetch_user_by_email(email)
            token = Token(user.unid)
            return {'status': 'true', 'token': token.token}
        

