from app.models.user import User
from app.models.user_team import UserTeam
from app.models.team import Team
from app.models.team_invite import TeamInvite
from flask_restful import Resource, reqparse
from app.resources.v1.base import BasicProtectedResource
from app.resources.v1.user import get_user
from app.resources.v1.team import get_team


class Invitations(BasicProtectedResource):

    invite_parser = reqparse.RequestParser()
    
    invite_parser.add_argument('team_unid', type=str, help='The team to invite a participant to', required=True, location='form')
    invite_parser.add_argument('invitee_unid', type=str, help='The team member type', required=False, location='form')
    invite_parser.add_argument('invitee_email', type=str, help='The email of a user to invite', required=False, location='form')
    
    get_invites_parser = reqparse.RequestParser()
    get_invites_parser.add_argument('user_unid', type=str, help='The user to query by', required=False, location="args")
    get_invites_parser.add_argument('team_unid', type=str, help='The team to query by', required=False, location="args")


    def post(self):
        args = self.invite_parser.parse_args()
        team_unid = args['team_unid']
        invitee_unid = args['invitee_unid']
        invitee_email = args['invitee_email']

        if not invitee_unid and not invitee_email:
            return {'status': 'false', 'message': 'Must invite by email or unid'}, 400
        
        if invitee_unid:
            user = get_user(invitee_unid)
        else:
            user = User.fetch_user_by_email(invitee_email)
            if not user:
                return {'status': 'false', 'message': 'No user found'}, 404

        team = get_team(team_unid)

        user_team_exist = UserTeam.get_user_team_by_user_and_team(invitee_unid, team.unid)

        if user_team_exist:
            return {'status': 'false', 'message': 'User already on that team'}, 400
invitation = TeamInvite(team_unid, invitee_unid)

        return {'status': 'true', 'message': 'Invitation sent successfully', 'invitation_unid': invitation.unid}, 201
    
    def get(self):
        args = self.get_invites_parser.parse_args()
        user_unid = args['user_unid']
        team_unid = args['team_unid']
        
        if team_unid:
            team = get_team(team_unid)
            result = TeamInvite.get_by_team_unid(team_unid)
        else:
            result = TeamInvite.get_invites()

        if user_unid:
            user = get_user(user_unid)
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
        status = args['status'].lower()
        
        invitation = TeamInvite.get_by_unid(invitation_unid)
        if invitation is None:
            return {'status': 'false', 'message': 'No invitation found'}, 404
    
        if status == 'accept':
            user_team = UserTeam(invitation.invite_user_unid, invitation.invite_team_unid, 1)
            invitation.delete(soft=False)
            Team.add_participant(invitation.invite_team_unid)
            return {'status': 'true', 'message': 'Invite accepted'}, 201
        elif status in ('decline', 'revoke'):
            invitation.delete(soft=False)
            return {'status': 'true', 'message': 'Invitation processed'}, 201
        else:
            return {'status': 'true', 'message': 'Invalid status'}, 400

