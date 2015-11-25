from app.models.token import Token
from app.auth import get_token
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource


class Logout(BasicProtectedResource):
    def post(self):
        token = get_token()
        
        found_token = Token.get_token(token)

        if found_token:
            found_token.expire_token()
            return {'status': 'true'}
        else:
            return {'status': 'false', 'message': 'Could not find token'}

