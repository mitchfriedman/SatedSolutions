from app.models.team import Team as TeamModel
from app.models.user_team import UserTeam
from app.models.user import User
from flask_restful import reqparse, abort
from app.resources.v1.base import BasicProtectedResource


def get_team(team_unid):
    team = TeamModel.get_team_by_unid(team_unid)
    if not team:
        abort(404, message='No team found', status='false')

    return team


def get_users_from_team(team_unid):
    members = UserTeam.get_users_teams_by_team(team_unid)
    users = [User.fetch_user_by_unid(member.user_unid) for member in members]
    users = [u for u in users if u is not None]
    serialized = []
    for member, user in zip(members, users):
        temp = user.serialize()
        temp['team_unid'] = member.team_unid
        serialized.append(temp)
    
    return serialized


class Teams(BasicProtectedResource):

    create_team_parser = reqparse.RequestParser()
    
    # create team arguments
    create_team_parser.add_argument('team_name', type=str, help='The team\'s name', required=True)
    create_team_parser.add_argument('team_captain', type=str, help='The Captain of the team', required=True)
    create_team_parser.add_argument('number_participants', type=int, help='Current number of participants', required=False)
    create_team_parser.add_argument('max_participants', type=int, help='The maximum number of participants', required=False)
    create_team_parser.add_argument('route_id', type=int, help='Route assigned to a team', required=False)
    create_team_parser.add_argument('requires_accessibility', type=int, help='Whether or not a team requires accessibility considerations', required=False)
    create_team_parser.add_argument('public_team', type=int, help='Whether or not this team is public', required=False)

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
        needs_accessibility = args.get('requires_accessibility', 0)
        public = args.get('public_team', 0)
        public = 0 if public == "0" or public == 0 or public == None else 1

        captain_user = User.fetch_user_by_unid(captain)
        
        if captain_user is None:
            return {'status': 'false', 'message': 'Team captain given does not exist'}, 400

        team = TeamModel.create_team(name, captain, max_members, num_members, public)

        user_team = UserTeam.add_user_to_team(captain, team.unid, 2)

        return {'status': 'true', 'team_id': team.unid, 'user_team': user_team.unid}, 201

    def get(self):
        args = self.get_teams_parser.parse_args()
        team_name = args.get('name', None)
        
        if team_name:
            teams = TeamModel.search_teams_by_name(name=team_name)
        else:
            teams = TeamModel.get_all_teams()
        
        team_data = [t.serialize() for t in teams]
    
        return {'teams': team_data}
    

class Team(BasicProtectedResource):
   
    update_instance_parser = reqparse.RequestParser()
    update_instance_parser.add_argument('team_unid', type=str, help="Team to update", required=True, location='view_args')
    update_instance_parser.add_argument('team_captain', type=str, help="New team captain", required=False)
    update_instance_parser.add_argument('number_participants', type=int, help='Change number of participants on team', required=False)
    update_instance_parser.add_argument('requires_accessibility', type=int, help='Require accessibility for this team', required=False)

    
    def get(self, team_unid):
        team = get_team(team_unid)

        users = get_users_from_team(team_unid)        
        team_serialized = team.serialize()
        team_serialized['users'] = users
        return {
            'team': team_serialized
        }, 200
        

    def post(self, team_unid):
        args = self.update_instance_parser.parse_args()
        team = get_team(team_unid)       

        team_captain = args.get('team_captain')
        if team_captain:
            team.team_captain = team_captain
        
        number_participants = args.get('number_participants')
        if number_participants:
            team.number_participants = number_participants

        requires_accessibility = args.get('required_accessibility')
        if requires_accessibility:
            team.requires_accessibility = requires_accessibility

        return {
            'team': {
                'unid': team.unid,
                'name': team.team_name,
                'captain': team.team_captain,
                'number_participants': team.number_participants,
                'requires_accessibility': str(team.requires_accessibility).lower(),
            }
        }, 200

