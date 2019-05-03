from sqlalchemy import Column, Boolean, Integer, Text
from database import Base
#from flask.ext.login import UserMixin

class Plants(Base):
    __tablename__= "plant"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=True, unique=False)
    german_name = Column(Text, nullable=True, unique=False)
    latin_name = Column(Text, nullable=False, unique=True)
    plant_information = Column(Text, nullable=True, unique=False)
    light = Column(Text, nullable=True, unique=False)
    watering = Column(Text, nullable=True, unique=False)
    placement = Column(Text, nullable=True, unique=False)
    insect_friendly = Column(Text, nullable=True, unique=False)
    other_information = Column(Text, nullable=True, unique=False)

class Pictures(Base):
    __tablename__= "pictures"
    picture_id
    plant_id
    picture_url
    picturepath = Column(Text, nullable=False)

'''
class User(Base):
    __tablename__= "user"
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
   

class Pictures(Base):
    __tablename__= "pictures"
    picture_id
    plant_id
    picture_url
    
    class Picture(Base):
    __tablename__ = "Bild"
    pictureID = Column(Integer, primary_key=True)
    picturepath = Column(Text, nullable=False)
    game_gamename = Column(Integer, ForeignKey("Spiel.gamename"))
    game = relationship("Game", backref=backref("computerspiele"))
    
    def __init__(self, pictureID=None, picturepath=None,  game_gamename=None):
        self.pictureID = pictureID
        self.picturepath = picturepath
        self.game_gamename = game_gamename
     
    '''