from app.models import base
from app.models.user import User
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import (
    Column,
    String,
    INTEGER,
    Boolean,
)
from app.utils.security import (
    encrypt,
)


class Team(base):
    __tablename__ = 'team'

    prefix = 'TE'

    team_name = Column(String(32), nullable=False)
    team_captain = Column(String(34))
    number_partcipants = Column(INTEGER)
    max_participants = Column(INTEGER)
    route_id = Column(INTEGER) # this should be a foreign key to the routes table
    requires_accessibility = Column(Boolean)
    public = Column(Boolean)

    def __init__(self, name, team_captain, max_participants, current_num_participants, public):
        self.team_name = name
        self.team_captain = team_captain or ''
        self.max_participants = max_participants or 10
        self.number_participants = current_num_participants or 0 # 1 for team captain, 0 for team with no captain
        self.route_id = 0
        self.requires_accessibility = False
        self.public = public

        self.init()

    @classmethod
    def create_team(cls, name, *args):
        team = Team(name, *args)
        return team

    @classmethod
    def get_teams_by_name(cls, name=None):
        return Team.get_list(team_name=name).all()

    @classmethod
    def get_team_by_unid(cls, team_unid):
        return Team.get_single(unid=team_unid)

    @classmethod
    def get_all_teams(cls):
        return Team.get_list().all()

