from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy
from app.models import BaseModel, base


def setup_engine(db_name=None, db_type=None,
                 username=None, password=None):
    db_type = db_type or "sqlite"

    # TODO setup postgres
    if db_type == "sqlite":
        uri = "sqlite:///tmp.db"

        db_options = {}

    return sqlalchemy.create_engine(uri, **db_options)


engine = None


def setup():  # TODO: pass a config object?
    global engine
    engine = setup_engine()
    Session = scoped_session(sessionmaker(bind=engine))
    BaseModel.query = Session.query_property()
    base.metadata.bind = engine


def stub():
    setup()
    base.metadata.create_all()
