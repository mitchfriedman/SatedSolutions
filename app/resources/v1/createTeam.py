from app.models.team import Team
from flask_restful import Resource, reqparse

class Team(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('team_name', type=str, help='The team\'s name', required=True)
    parser.add_argument('team_captain', type=str, help='The Captain of the team', required=False)
    parser.add_argument('number_participants', type=int, help='Current number of participants', required=False)
    parser.add_argument('max_participants', type=int, help='The maximum number of participants', required=False)
    parser.add_argument('route_id', type=int, help='Route assigned to a team', required=False)
    parser.add_argument('requires_accessibility', type=bool, help='Whether or not a team requires accessibility considerations', required=False)

    def post(self):
        args = self.parser.parse_args()
        name = args['team_name']
        max_members = args['max_participants']
        captain = args['team_captain']
        num_members = args['number_participants']
        route = args['route_id']
        needs_accessibility = args['requires_accessibility']

        return {'status': 'true'}, 201
    
