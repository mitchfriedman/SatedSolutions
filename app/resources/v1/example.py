from app.models.user import User
from flask_restful import Resource, reqparse


class Sample(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='An email to create an account with', required=True)
    parser.add_argument('password', type=str, help='A password to create the account with', required=True)
    
    
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        user = User.create_user(email, password)

        return {'user': {
                'email': user.email,
                'unid': user.unid, # this is magical...
            }
        }
    
