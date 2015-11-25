from app.auth import get_token, authenticate, get_user_unid
from app.models.token import Token
from tests.base import TestCase
from flask import Flask
from nose.tools import raises


app = Flask(__name__)

@authenticate
def authenticated_function():
    return True

class TestAuthentication(TestCase):
    
    def test_get_auth_token_with_headers(self):
        with app.test_request_context('/', headers={'Authentication': 'foo'}):
            self.assertEqual('foo', get_token())

    def test_get_auth_token_no_headers(self):
        with app.test_request_context('/'):
            self.assertEqual(None, get_token())
    
    @raises(Exception)
    def test_token_authentication_without_headers(self):
        token = Token('user123')
        with app.test_request_context('/'):
            return_value = authenticated_function()

    def test_token_authentication_with_headers(self):
        token = Token('user123')
        with app.test_request_context('/', headers={'Authentication': token.token}):
            return_value = authenticated_function()
            self.assertTrue(return_value)
            found_token = get_token()
            self.assertEqual(token.token, found_token)

            user_unid = get_user_unid(found_token)
            self.assertEqual('user123', user_unid)

