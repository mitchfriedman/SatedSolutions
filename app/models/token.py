from app.models import base
import datetime, uuid
from sqlalchemy import  (
    Column,
    String,
    INTEGER,
    DateTime,
    Boolean,
)


class Token(base):
    __tablename__ = 'token'

    prefix = 'TO'

    LIFESPAN = 360000

    token = Column(String(128))
    expiry_time = Column(DateTime)
    user_unid = Column(String(34))
    expired = Column(Boolean)

    def __init__(self, user_unid):
        self.token = self.generate_random_token()
        self.user_unid = user_unid
        self.init()
        self.expired = False
        self.update_expiry()


    def update_expiry(self, seconds_delta=None):
        seconds_delta = seconds_delta or self.LIFESPAN
        self.expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds_delta)
        self.save()

    def generate_random_token(self):
        return uuid.uuid4().hex + uuid.uuid4().hex

    @classmethod
    def get_token(cls, token):
        return Token.get_single(token=token)

    def expire_token(self):
        self.delete(soft=False)

    def is_valid(self):
        return self.expiry_time > datetime.datetime.now()

