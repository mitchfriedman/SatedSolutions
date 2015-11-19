from app.models import base
from sqlalchemy import (
    Column,
    String,
    INTEGER,
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
    account_type = Column(INTEGER)

    account_mappings = {
        1: 'Participant',
        2: 'Captain',
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.init()

    @classmethod
    def create_user(cls, email, password):
        password = encrypt(password)
        user = User(email, password)

        return user

    @classmethod
    def fetch_user_by_email(cls, email):
        return User.get_single(email=email)

    @classmethod
    def fetch_user_by_unid(cls, unid):
        return User.get_single(unid=unid)
    
    @classmethod
    def authenticate(cls, email, password):
        user = cls.fetch_user_by_email(email)
        return verify_password(password, user.password) if user else False

