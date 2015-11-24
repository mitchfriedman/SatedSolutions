from app.models.token import Token
from flask_restful import Resource, reqparse


class Logout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str, help='The token of the session to expire', required=True)

    def post(self):
        args = self.parser.parse_args()
        token = args['token']
        
        found_token = Token.get_token(token)
        print(found_token)

        if found_token:
            found_token.expire_token()
            return {'status': 'true'}
        else:
            return {'status': 'false', 'message': 'Could not find token'}

