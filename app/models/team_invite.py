from app.models import base
from sqlalchemy import (
    Column,
    String,
    INTEGER,
)


class TeamInvite(base):
    __tablename__ = 'team-invite'
    
    prefix = 'TI'

    invite_team_unid = Column(String(34))
    invite_user_unid = Column(String(34))
    invited_user_email = Column(String(128))
    rejected = Column(INTEGER)

    def __init__(self, invite_team_unid, invite_user_unid, invited_user_email):
        self.invite_team_unid = invite_team_unid
        self.invite_user_unid = invite_user_unid
        self.invited_user_email = invited_user_email
        self.rejected = 0
        self.init()

    def serialize(self):
        return {
            'invite_team_unid': self.invite_team_unid,
            'invite_user_unid': self.invite_user_unid,
            'status': 'pending',
            'unid': self.unid,
        }

    @classmethod
    def get_by_unid(cls, invite_unid):
        return TeamInvite.get_single(unid=invite_unid)

    @classmethod
    def send_invitation(cls, team, inviter_unid, invitee_email):
        return TeamInvite(team, inviter_unid, invitee_email)

    def accept_invite(self):
        self.rejected = 0
        self.delete(soft=False)

    def reject_invite(self):
        self.rejected = 1
        self.delete(soft=False)

    @classmethod
    def get_by_team_unid(cls, team_unid):
        return TeamInvite.get_list(invite_team_unid=team_unid)

    @classmethod
    def get_by_user_unid(cls, user_unid):
        return TeamInvite.get_list(invite_user_unid=user_unid)

    @classmethod
    def get_invites(cls):
        return TeamInvite.get_list()
    
