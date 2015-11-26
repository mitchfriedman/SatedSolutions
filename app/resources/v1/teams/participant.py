from app.models.user_team import UserTeam
from flask_restful import reqparse
from app.resources.v1.base import BasicProtectedResource


class Participants(BasicProtectedResource):
    create_parser = reqparse.RequestParser()
    
    create_parser.add_argument('user_unid', type=str, help='The user to add to the team', required=True)
    create_parser.add_argument('member_type', type=int, help='The team member type', required=False)

    
    def post(self, team_unid):
        args = create_parser.parse_args()
        user_unid = args['user_unid']
        member_type = args.get('member_type', 1) # default value of 1 (participant)

        team = Team.get_team_by_unid(team_unid)

        if not team:
            return {'status': 'false', 'message': 'Invalid team unid'}
        
        user = User.fetch_by_unid(user_unid)

        if not user:
            return {'status': 'false', 'message': 'Invalid user unid'}

        user_team = UserTeam.add_user_to_team(user_unid, team_unid, member_type)

        return {'status': 'true', 'user_team_unid': user_team.unid, 'team': team.serialize()}

