from app.models import base
from sqlalchemy import (
    Column,
    String,
    INTEGER,
)


class Route(base):
    __tablename__ = 'route'

    prefix = 'RO'
    
    time = Column(String(128))
    route_type = Column(String(16))
    accessibility = Column(String(6))
    name = Column(String(64))
    origin_point = Column(String(256))
    destination_point = Column(String(256))

    def __init__(self, name, origin, destination, time, route_type, accessibility):
        self.name = name
        self.origin_point = origin
        self.destination_point = destination
        self.time = time
        self.route_type = route_type
        self.accessibility = accessibility

        self.init()

    def serialize(self):
        return {
            'unid': self.unid,
            'origin_point': self.origin_point,
            'destination_point': self.destination_point,
            'time': self.time,
            'route_type': self.route_type,
            'name': self.name,
            'accessibility': self.accessibility,
        }

    @classmethod
    def get_routes(cls, **kwargs):
        return Route.get_list(**kwargs).all()
    
    @classmethod
    def get_route_by_unid(cls, unid):
        return Route.get_single(unid=unid)
