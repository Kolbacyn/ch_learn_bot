from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class Word(Base):
    """Model for word"""
    word = Column(String)
    transcription = Column(String)
    rus_translation = Column(String)
    level = Column(Integer)
