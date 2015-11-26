from app.models import base
from sqlalchemy import (
    Column,
    String,
)


class UserTeam(base):
    __tablename__ = 'user-teams'

    prefix = 'UT'

    user_unid = Column(String(34))
    team_unid = Column(String(34))
    
    member_type = Column(INTGER)

    member_mappings = {
        1: 'Participant',
        2: 'Team Captain'
    }

    def __init__(self, user_unid, team_unid, member_type):
        self.user_unid = user_unid
        self.team_unid = team_unid
        self.member_type = member_type
    
    @classmethod
    def add_user_to_team(cls, user_unid, team_unid, member_type):
        return UserTeam(user_unid, team_unid, member_type)

    @classmethod
    def get_user_unids_by_team(cls, team_unid):
        return UserTeam.get_list(team_unid=team_unid).all()

