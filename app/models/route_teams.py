from app.models import base
from sqlalchemy import (
    Column,
    String,
    INTEGER,
)


class RouteTeam(base):
    __tablename__ = 'route-teams'

    prefix = 'UT'

    route_unid = Column(String(34))
    team_unid = Column(String(34))

    def __init__(self, route_unid, team_unid):
        self.route_unid = route_unid
        self.team_unid = team_unid

        self.init()

    def serialize(self):
        return  {'route_unid': self.route_unid, 'team_unid': self.team_unid, 'unid': self.unid}
    
    @classmethod
    def get_team_route(cls, team_unid):
        return RouteTeam.get_single(team_unid=team_unid)

