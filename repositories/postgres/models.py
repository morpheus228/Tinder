import enum
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
    __tablename__ = 'UserForms'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.id'))
    name = Column(String(64))
    about = Column(String(1024))
    request = Column(String(256))
    photo_1 = Column(String(256))
    created_at = Column(DateTime(), default=datetime.utcnow)
