from sqlalchemy import create_engine
engine = create_engine('sqlite:///bus_booking.db',echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, String, Integer,MetaData, Table

def create_table(**kwargs):
    
    zopper_data = Table("zopper_data", MetaData,
                        Column(,)

class Zopper(Base):
    __tablename__ = 'zopper'
    device_idn = Column(Integer, primary_key=True)
    device_name = Column(String(250))
    gmnification = Column(String(50))
    field_of_view = Column(String(50))
    range = Column(String(50))


Base.metadata.create_all(engine)
