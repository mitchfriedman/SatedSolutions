from app.models.route import Route as RouteModel
from flask_restful import reqparse, abort
from app.resources.v1.base import BasicProtectedResource


def get_route(route_unid):
    route = RouteModel.get_route_by_unid(route_unid)
    if not route:
        abort(404, message='No route found', status='false')

    return route


class Routes(BasicProtectedResource):
    get_routes_parser = reqparse.RequestParser()
    
    def get(self):
        routes = RouteModel.get_routes()

        return {
            'routes': [route.serialize() for route in routes]
        }

