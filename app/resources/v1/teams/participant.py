from app.models.user_team import UserTeam
from app.models.team import Team
from app.models.user import User
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource
from app.resources.v1.team import get_users_from_team, get_team
from app.resources.v1.user import get_user


class Participants(BasicProtectedResource):
    create_parser = reqparse.RequestParser()
    
    create_parser.add_argument('user_unid', type=str, help='The user to add to the team', required=True)
    create_parser.add_argument('member_type', type=int, help='The team member type', required=False)

    
    def post(self, team_unid):
        args = self.create_parser.parse_args()
        user_unid = args['user_unid']
        member_type = args['member_type']

        team = get_team(team_unid)
        
        user = get_user(user_unid)

        user_team = UserTeam.add_user_to_team(user_unid, team_unid, member_type)
        if user_team.member_type == 2:
            team.team_captain = user_team.user_unid
        team.number_participants += 1

        return {'status': 'true', 'user_team_unid': user_team.unid, 'team': team.serialize()}

    def get(self, team_unid):
        team = get_team(team_unid)

        return {'users': get_users_from_team(team_unid)}
    
    
class Participant(BasicProtectedResource):

    def get(self, team_unid, user_unid):
        team = get_team(team_unid)

        user = get_user(user_unid)

        user_team = UserTeam.get_user_team_by_user_and_team(user_unid, team_unid)
    
        return {
            'status': 'true',
            'user_type': user_team.member_mappings.get(user_team.member_type, 'Participant'),
        }


    def delete(self, team_unid, user_unid):
        team = get_team(team_unid)

        user = get_user(user_unid)

        user_team = UserTeam.get_user_team_by_user_and_team(user_unid, team_unid)

        if not user_team:
            return {'status': 'false', 'message': 'The given user is not on that team'}, 400
        
        is_captain = user_team.member_type == 2
        user_team.delete(soft=False)
        new_captain = None
        team.number_participants -= 1

        if is_captain:
            new_captain = UserTeam.get_oldest_team_member(team_unid)

        if new_captain:
            new_captain.member_type = 2
            team.team_captain = new_captain.unid

        return {}, 204

