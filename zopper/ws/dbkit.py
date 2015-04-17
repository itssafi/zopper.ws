"""
This module use to create session
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CreateSession:
    session = None

    @classmethod
    def createsession(cls):
        if cls.session == None:
            engine = create_engine('sqlite:///zopper.db',echo=False)
            conn = engine.connect()
            Session = sessionmaker(bind=engine)
            session = Session()
            cls.session = session
        return cls.session


class SessionCommit(object):

    def __init__(self, session):
        self.session = session

    def commit(self, flag=False):
        if flag:
            self.session.commit()
