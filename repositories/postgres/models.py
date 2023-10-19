from sqlalchemy import BigInteger, String, Column, DateTime, ForeignKey, Boolean, Integer, Text, Float, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime(), default=datetime.utcnow)


class Form(Base):
    __tablename__ = 'Forms'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.id', ondelete='CASCADE'))
    username = Column(String(256))
    gender = Column(Boolean)
    name = Column(String(64))
    faculty = Column(String(64))
    course = Column(String(64))
    about = Column(String(1024))
    request = Column(String(256))
    photo_1 = Column(String(256))
    photo_2 = Column(String(256))
    photo_3 = Column(String(256))
    video = Column(String(256))
    created_at = Column(DateTime(), default=datetime.utcnow)


class Rate(Base):
    __tablename__ = 'Rates'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.id', ondelete='CASCADE'))
    form_id = Column(BigInteger, ForeignKey('Forms.id', ondelete='CASCADE'))
    value = Column(Boolean, default=False)    
    created_at = Column(DateTime(), default=datetime.utcnow)


class Match(Base):
    __tablename__ = 'Matches'

    id = Column(BigInteger, primary_key=True)
    liker_rate_id = Column(BigInteger, ForeignKey('Rates.id', ondelete='CASCADE'))
    getter_rate_id = Column(BigInteger, ForeignKey('Rates.id', ondelete='CASCADE'))
    result = Column(Boolean, nullable=True)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)