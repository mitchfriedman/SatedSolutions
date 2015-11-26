from app.models.user import User
from app.models.user_team import UserTeam
from app.models.team import Team
from app.models.team_invite import TeamInvite
from flask_restful import Resource, reqparse
from app.resources.v1.base import BasicProtectedResource

class Invitations(BasicProtectedResource):

    invite_parser = reqparse.RequestParser()
    
    invite_parser.add_argument('team_unid', type=str, help='The team to invite a participant to', required=True)
    invite_parser.add_argument('inviter_unid', type=str, help='The participant who sent the invitation', required=True)
    invite_parser.add_argument('invitee_email', type=str, help='The team member type', required=True)
    
    get_invites_parser = reqparse.RequestParser()
    get_invites_parser.add_argument('user_unid', type=str, help='The user to query by', required=False, location="args")
    get_invites_parser.add_argument('team_unid', type=str, help='The team to query by', required=False, location="args")

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

        return {'status': 'true', 'message': 'Invitation sent successfully', 'invitation_unid': invitation.unid}, 201
    
    def get(self):
        args = self.get_invites_parser.parse_args()
        user_unid = args['user_unid']
        team_unid = args['team_unid']
        
        if team_unid:
            team = Team.get_team_by_unid(team_unid)
            if not team:
                return {'status': 'false', 'message': 'No team found'}
        
            result = TeamInvite.get_by_team_unid(team_unid)
        else:
            result = TeamInvite.get_invites()

        if user_unid:
            user = User.fetch_user_by_unid(user_unid)
            if not user:
                return {'status': 'false', 'message': 'No user found'}
            team_invites = result.filter_by(invite_user_unid=user_unid)
        else:
            team_invites = result
        
        invites_serialized = [invite.serialize() for invite in team_invites]
        return {
            'invites': invites_serialized
        }, 200


class Invitation(BasicProtectedResource):

    update_parser = reqparse.RequestParser()
    
    update_parser.add_argument('status', type=str, help='The status of the invitation', required=True)

   
    def get(self, invitation_unid):
        invitation = TeamInvite.get_by_unid(invitation_unid)

        if not invitation:
            return {'status': 'false', 'message': 'No invitation found'}, 404
 
        return {'invitation': invitation.serialize()},200

    def post(self, invitation_unid):
        args = self.update_parser.parse_args()
        status = args['status']
        
        invitation = TeamInvite.get_by_unid(invitation_unid)
        if invitation is None:
            return {'status': 'false', 'message': 'No invitation found'}, 404

        if status.lower() == 'accept':
            user_team = UserTeam(invitation.invite_user_unid, invitation.invite_team_unid, 1)
            invitation.delete(soft=False)
            team = Team.get_team_by_unid(invitation.invite_team_unid)
            team.number_participants += 1
            return {'status': 'true', 'message': 'Invite accepted'}, 201
        elif status.lower() == 'decline' or status.lower() == 'revoke':
            invitation.delete(soft=False)
            return {'status': 'true', 'message': 'Invitation processed'}, 201

