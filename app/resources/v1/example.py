from flask_restful import Resource, reqparse


class Sample(Resource):
    
    def get(self):
        return {'hello': 'world'}

    
