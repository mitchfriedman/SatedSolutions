ERROR_CODES = {
    'EmailTaken': {
        'message': 'A user with that email already exists in the database.',
        'code': 409,
        'extra': 'Try logging in instead'
    },
}

class Error(Exception):
    def __init__(self, error_name, extra=None):
        self.error_name = error_name
        self.extra = extra
 

class ApiError(Error):
    def __init__(self, error_name, extra=None):
        super(ApiError, self).__init__(error_name, extra)


class BackendError(Error):
    def __init__(self, error_name, extra=None):
        super(BackendError, self).__init__(error_name, extra)


class AuthorizationError(Error):
    def __init__(self, error_name, extra=None):
        super(AuthorizationError, self).__init__(error_name, extra)


def get_error(error_type):
    error = ERROR_CODES.get(error_type, ERROR_CODES.get('RunTimeError'))

    return error

