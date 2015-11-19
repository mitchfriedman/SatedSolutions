from flask_restful import Api
from app.errors import get_error


class RestApi(Api):
    def __init__(self, *args, **kwargs):
        kwargs['catch_all_404s'] = True
        super(RestApi, self).__init__(*args, **kwargs)

    def handle_error(self, e):
        error = get_error(str(e))
        if error is not None:
            return self.make_response(error, error.get('code'))

        return super(RestApi, self).handle_error(e)

def abort(error):
    raise Exception(error)

