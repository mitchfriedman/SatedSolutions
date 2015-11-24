from app.apis import Api
from app.resources.v1.example import Sample
from app.resources.v1.login import Login
from app.resources.v1.register import Register
from app.resources.v1.logout import Logout


api = Api()


api.add_resource(Sample, '/api/Sample')
api.add_resource(Login, '/api/Login')
api.add_resource(Register, '/api/Register')
api.add_resource(Logout, '/api/Logout')

