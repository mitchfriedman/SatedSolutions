from app.models import base
from app.models.user import User
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import (
    Column,
    String,
    INTEGER,
    Boolean,
)


class Team(base):
    __tablename__ = 'team'

    prefix = 'TE'

    team_name = Column(String(32), nullable=False)
    team_captain = Column(String(34))
    number_participants = Column(INTEGER)
    max_participants = Column(INTEGER)
    route_id = Column(INTEGER) # this should be a foreign key to the routes table
    requires_accessibility = Column(Boolean)
    public = Column(INTEGER)

    def __init__(self, name, team_captain, max_participants, current_num_participants, public):
        self.team_name = name
        self.team_captain = team_captain or ''
        self.max_participants = max_participants or 10
        self.number_participants = current_num_participants or 1 # 1 for team captain, 0 for team with no captain
        self.route_id = 0
        self.requires_accessibility = False
        self.public = public

        self.init()

    def serialize(self):
        return {
            'team_name': self.team_name,
            'unid': self.unid,
            'number_participants': self.number_participants,
            'public': str(self.public).lower(),
            'captain': self.team_captain,
        }

    @classmethod
    def create_team(cls, name, *args):
        team = Team(name, *args)
        return team

    @classmethod
    def get_teams_query(cls):
        return Team.get_list(public=1).order_by(cls.team_name.asc()) 

    @classmethod
    def get_teams_by_name(cls, name=None):
        return cls.get_teams_query().filter_by(name=name)

    @classmethod
    def search_teams_by_name(cls, name=None):
        return cls.get_teams_query().filter(cls.team_name.like("%{}%".format(name))).all()

    @classmethod
    def get_team_by_unid(cls, team_unid):
        return Team.get_single(unid=team_unid)

    @classmethod
    def get_all_teams(cls):
        return cls.get_teams_query().all()
    
    @classmethod
    def add_participant(cls, unid):
        team = cls.get_team_by_unid(unid)
        team.number_participants += 1
