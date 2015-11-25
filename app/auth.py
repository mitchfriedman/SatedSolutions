from functools import wraps
from flask import request, abort, g
from app.models.token import Token


def do_authentication(func, *args, **kwargs):
    token = get_token()

    if token:
        authentication = token_authentication(token)
        if authentication.get('authorized') == True:
            g.authentication = authentication
            
            return func(*args, **kwargs)
    
    abort(401, "Invalid Authentication token")


def get_token():
    return request.headers.get('Authentication')


def get_user_unid(token):
    return Token.get_token(token).user_unid


def token_authentication(token):
    token_instance = Token.get_token(token)
    if not token_instance or not token_instance.is_valid():
        abort(401, 'Invalid Authentication token')

    return {
        'authorized': True, 
        'token': token
    }


def authenticate(func):
    """
    Method decorator for authenticating a user by
    the given token. Used in flask_restful resources 
    requiring authentication.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return do_authentication(func, *args, **kwargs)

    return wrapper
