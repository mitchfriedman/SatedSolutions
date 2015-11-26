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

    @classmethod
    def send_invitation(cls, team, inviter_unid, invitee_email):
        return TeamInvite(team, inviter_unid, invitee_email)

    @classmethod
    def accept_invite(self):
        self.rejected = 0
        self.delete()

    @classmethod
    def reject_invite(self):
        self.rejected = 1
        self.delete()
