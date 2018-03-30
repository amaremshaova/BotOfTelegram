from sqlalchemy import Column, String, Integer, DateTime,  ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import json
from sqlalchemy import create_engine
import os.path
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class Channel(Base):
    __tablename__ = 'channels'
    id_channel = Column(Integer, primary_key=True)
    name = Column(String)
    tv_programs = relationship("TVprogram", backref='channels', lazy = 'joined')

class Telecast(Base):
    __tablename__ = 'telecasts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tv_programs = relationship("TVprogram", backref='telecasts', lazy = 'joined')
    genre = Column(Integer, ForeignKey('genres.id'), index =True)
        
class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telecasts = relationship("Telecast", backref='genres', lazy = 'joined')    
        

class TVprogram(Base):
    __tablename__ = 'tv_program'
    channel = Column(Integer, ForeignKey('channels.id_channel'), primary_key=True)
    telecast = Column(Integer, ForeignKey('telecasts.id'), index = True)
    start_time = Column(DateTime, primary_key = True)
    end_time = Column(DateTime)

def create_table():
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\data_connection.json', 'r', encoding = 'utf-8') as file_json:
       data = json.load(file_json)
    
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(data['user'],data['password'],data['host'],data['port'],data['database']))

    metadata = MetaData()
    metadata = Base.metadata
    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session

