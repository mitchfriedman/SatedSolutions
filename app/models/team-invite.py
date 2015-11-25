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


    def __init__(self, invite_team_unid, invite_user_unid, invited_user_email):
        self.invite_team_unid = invite_team_unid
        self.invite_user_unid = invite_user_unid
        self.invited_user_email = invited_user_email

        self.init()

    def accept_invite(self):
        self.delete()

    def reject_invite(self):
        self.delete()

