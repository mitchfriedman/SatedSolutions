from sqlalchemy import Boolean, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid, datetime


class ModelMixin(object):

    prefix = None

    auto_id = Column(Integer, primary_key=True, autoincrement=True)

    date_created = Column(DateTime, nullable=False)
    date_updated = Column(DateTime, nullable=False)

    alive = Column(Boolean)
    unid = Column(String(34))

    @classmethod
    def get_single(cls, **kwargs):
        return cls.get_list(**kwargs).first()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        return cls.init(instance)

    @classmethod
    def get_list(cls, **kwargs):
        newest = kwargs.pop('newest', None)

        query = cls.query.filter_by(**kwargs)

        if newest:
            query = cls.newest(query)

        return query

    @classmethod
    def paginate(cls, query, limit, offset):
        return query.limit(limit).offset(offset)

    @classmethod
    def get_list_paginated(cls, **kwargs):
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)

        return cls.get_list(**kwargs).limit(limit).offset(offset)

    @classmethod
    def newest(cls, query):
        return query.order_by(cls.date_updated.desc())

    def init(self):
        self.unid = self.generate_unid()
        self.date_created = datetime.datetime.now()
        self.alive = True

        return self.save()

    def update(self, commit: bool=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        return commit and self.save() or self

    def save(self, commit: bool=True):
        self.query.session.add(self)
        self.date_updated = datetime.datetime.now()

        if commit:
            self.query.session.commit()
        return self

    def delete(self, soft: bool=True, commit: bool=True):
        deleted = self._soft_delete() if soft else self._hard_delete()

        if commit:
            self.query.session.commit()

        return deleted

    def _hard_delete(self):
        self.query.session.delete(self)
        return None

    def _soft_delete(self):
        self.alive = False
        return self

    @classmethod
    def generate_unid(cls):
        if cls.prefix is None:
            raise NotImplementedError()

        unid = cls.prefix + uuid.uuid4().hex

        while len(cls.get_list(unid=unid).all()) > 0:
            unid = cls.prefix + uuid.uuid4().hex

        return unid


class BaseModel(ModelMixin):
    __table_args__ = {'extend_existing': True}
    __abstract__ = True


base = declarative_base(cls=BaseModel)
