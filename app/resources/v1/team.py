from app.models.team import Team
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource


class Teams(BasicProtectedResource):

    create_team_parser = reqparse.RequestParser()
    
    # create team arguments
    create_team_parser.add_argument('team_name', type=str, help='The team\'s name', required=True)
    create_team_parser.add_argument('team_captain', type=str, help='The Captain of the team', required=False)
    create_team_parser.add_argument('number_participants', type=int, help='Current number of participants', required=False)
    create_team_parser.add_argument('max_participants', type=int, help='The maximum number of participants', required=False)
    create_team_parser.add_argument('route_id', type=int, help='Route assigned to a team', required=False)
    create_team_parser.add_argument('requires_accessibility', type=bool, help='Whether or not a team requires accessibility considerations', required=False)

    get_teams_parser = reqparse.RequestParser()

    # search teams
    get_teams_parser.add_argument('name', type=str, help='The team name to search', required=False)


    def post(self):
        args = self.create_team_parser.parse_args()
        name = args['team_name']
        max_members = args['max_participants']
        captain = args['team_captain']
        num_members = args['number_participants']
        route = args['route_id']
        needs_accessibility = args['requires_accessibility']

        team = Team.create_team(name, captain, max_members, num_members)

        return {'status': 'true', 'team_id': team.unid}, 201

    def get(self):
        args = self.get_teams_parser.parse_args()
        
        team_name = args.get('name', None)
        
        if team_name:
            teams = Team.get_teams_by_name(name=team_name)
        else:
            teams = Team.get_all_teams()
        
        team_data = [
            {
                'unid': t.unid,
                'name': t.team_name, 
                'captain': t.team_captain, 
            }
            for t in teams
        ]
    
        return {'teams': team_data}

