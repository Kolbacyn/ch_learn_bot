from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class PreBase:

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        """Returns table name from class name."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Word(Base):
    """Model for word"""
    word = Column(String)
    transcription = Column(String)
    rus_translation = Column(String)
    level = Column(Integer)
