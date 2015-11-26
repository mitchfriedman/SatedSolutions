from app.models.user import User
from app.models.team import Team
from app.models.team_invite import TeamInvite
from app.models.user_team import UserTeam
from flask_restful import Resource, reqparse
from app.resources.v1.base import BasicProtectedResource

class Invitations(BasicProtectedResource):

    invite_parser = reqparse.RequestParser()
    
    invite_parser.add_argument('team_unid', type=str, help='The team to invite a participant to', required=True)
    invite_parser.add_argument('inviter_unid', type=str, help='The participant who sent the invitation', required=True)
    invite_parser.add_argument('invitee_email', type=str, help='The team member type', required=True)
    invite_parser.add_argument('rejected', type=int, help='Rejected Status', required=False)
    
    get_invites_parser = reqparse.RequestParser()
    get_invites_parser.add_argument('user_unid', type=str, help='The user to query by', required=False)

    def post(self):
        args = self.invite_parser.parse_args()
        team_unid = args['team_unid']
        inviter_unid = args['inviter_unid']
        invitee_email = args.get('invitee_email') # default value of 1 (participant)

        if not invitee_email:
            return {'status': 'false', 'message': 'Invalid invitee email'}
        
        user = User.fetch_user_by_unid(inviter_unid)

        if not user:
            return {'status': 'false', 'message': 'Invalid inviter unid'}

        team = UserTeam.get_team_by_user(inviter_unid)

        invitation = TeamInvite.send_invitation(team_unid, inviter_unid, invitee_email)

        return {'status': 'true', 'message': 'Invitation sent successfully'}
    
    def get(self):
        args = self.get_invites_parser.parse_args()
        user_unid = args['user_unid']
        if user_unid:
            user = User.fetch_user_by_unid(user_unid)
            if not user:
                return {'status': 'false', 'message': 'No user found'}
            team_invites = TeamInvite.get_by_user_unid(user_unid)
        else:
            team_invites = TeamInvite.get_invites()
        
        invites_serialized = [invite.serialize() for invite in team_invites]
        return {
            'invites': invites_serialized
        }

