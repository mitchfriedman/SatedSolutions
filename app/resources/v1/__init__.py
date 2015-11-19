from app.apis import Api
from app.resources.v1.example import Sample


api = Api()


api.add_resource(Sample, '/api/Sample')

