from app.apis import Api
from app.resources.v1.example import Sample
from app.resources.v1.authentication import Login


api = Api()


api.add_resource(Sample, '/api/Sample')
api.add_resource(Login, '/api/Login')

