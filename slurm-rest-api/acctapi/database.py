# taken from http://flask.pocoo.org/docs/0.11/patterns/sqlalchemy/#declarative

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine('mysql://%s:%s@%s/%s' %(
    config.database['db_user'],
    config.database['db_pass'],
    config.database['db_host'],
    config.database['db_name']
))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    from models import Job,Assoc
    try:
        Base.metadata.create_all(bind=engine)
    except exc.SQLAlchemyError as e:
        print("Error encountered while connecting to acct_db:" + e.message)
