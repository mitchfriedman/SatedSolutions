from app.models.route_teams import RouteTeam
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource
from app.resources.v1.team import get_team
from app.resources.v1.route import get_route


class TeamRoutes(BasicProtectedResource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('route_unid', type=str, help='The route to set the team to', required=True)

    def post(self, team_unid):
        args = self.parser.parse_args()
        team = get_team(team_unid)
        route_unid = args['route_unid']
        route = get_route(route_unid)

        found = RouteTeam.get_team_route(team_unid)
        if found:
            found.delete(soft=False)

        route_team = RouteTeam(route_unid, team_unid)

        return {'status': 'true', 'route_team_unid': route_team.unid}, 201

    def get(self, team_unid):
        team = get_team(team_unid)
        
        route = RouteTeam.get_team_route(team_unid)
        return {'status': 'true', 'route': route.serialize() if route else None}

