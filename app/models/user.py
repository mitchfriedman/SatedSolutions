from app.models import base
from sqlalchemy import (
    Column,
    String,
    INTEGER,
    Boolean,
)
from app.utils.security import (
    encrypt,
    verify_password,
)



class User(base):
    __tablename__ = 'user'

    prefix = 'US'

    email = Column(String(128))
    password = Column(String(256))
    first = Column(String(64))
    last = Column(String(64))
    age_check = Column(Boolean)
    account_type = Column(INTEGER)

    account_mappings = {
        1: 'Participant',
        2: 'Captain',
    }

    def __init__(self, email, password, first, last, age_check):
        self.email = email
        self.password = password
        self.first = first
        self.last = last
        self.age_check = age_check

        self.init()

    def serialize(self):
        return {
            'unid': self.unid,
            'email': self.email,
            'first': self.first,
            'last': self.last,
            'over_12': self.age_check,
            'date_created': str(self.date_created),
        }

    @classmethod
    def create_user(cls, email, password, *args):
        password = encrypt(password)
        user = User(email, password, *args)

        return user

    @classmethod
    def fetch_user_by_email(cls, email):
        return User.get_single(email=email)

    @classmethod
    def get_all_users(cls):
        return User.get_list().all()

    @classmethod
    def fetch_user_by_unid(cls, unid):
        return User.get_single(unid=unid)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.fetch_user_by_email(email)
        return verify_password(password, user.password) if user else False

