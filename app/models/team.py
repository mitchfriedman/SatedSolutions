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

    prefix = 'T'

    team_name = Column(String(32), nullable=False)
    team_captain = Column(INTEGER, ForeignKey('user.unid'))
    number_partcipants = Column(INTEGER)
    max_participants = Column(INTEGER)
    route_id = Column(INTEGER) #this should be a foreign key to the routes table
    requires_accessibility = Column(Boolean)

    def __init__(self, name, team_captain, max_participants, current_num_participants):
        self.team_name = name
        self.team_captain = team_captain
        self.max_participants = max_participants
        self.number_participants = current_num_participants #1 for team captain, 0 for team with no captain
        self.route_id = 0
        self.requires_accessibility = False
        self.init()

    @classmethod
    def create_team(cls, name, *args):
        team = Team(name, *args)
        return team












