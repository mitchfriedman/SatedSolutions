from app.models.user import User
from app.models.team import Team
from app.models.team_invite import TeamInvite
from app.models.user_team import UserTeam
from flask_restful import Resource, reqparse
from app.resources.v1.base import BasicProtectedResource

class Invitation(BasicProtectedResource):

    invite_parser = reqparse.RequestParser()
    
    invite_parser.add_argument('inviter_unid', type=str, help='The participant who sent the invitation', required=True)
    invite_parser.add_argument('invitee_email', type=str, help='The team member type', required=True)
    invite_parser.add_argument('rejected', type=int, help='Rejected Status', required=False)
    
    def post(self, team_unid):
        args = self.invite_parser.parse_args()
        inviter_unid = args['inviter_unid']

        invitee_email = args.get('invitee_email') # default value of 1 (participant)

        if not invitee_email:
            return {'status': 'false', 'message': 'Invalid invitee email'}
        
        user = User.fetch_user_by_unid(inviter_unid)

        if not user:
            return {'status': 'false', 'message': 'Invalid inviter unid'}

        team = UserTeam.get_team_by_user(inviter_unid)

        invitation = TeamInvite.send_invitation(team, inviter_unid, invitee_email)

        return {'status': 'true', 'message': 'Invitation sent successfully'}
