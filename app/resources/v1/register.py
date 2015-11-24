from app.models.user import User
from flask_restful import Resource, reqparse


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='The email to register with', required=True)
    parser.add_argument('password', type=str, help='The password for the account', required=True)
    parser.add_argument('first', type=str, help='The first name for account', required=True)
    parser.add_argument('last', type=str, help='The last name for account', required=True)
    parser.add_argument('ageCheck', type=str, help='Indicating if this person is over 12.', required=False)

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']
        first = args['first']
        last = args['last']
        age_check = args['ageCheck']

        if User.fetch_user_by_email(email) is not None:
            return {"status": "false"}, 400

        user = User.create_user(email, password, first, last, age_check)
        
        if user:
            return {'status': 'true'}, 201
        else:
            return {'status': 'false'}, 400
    
