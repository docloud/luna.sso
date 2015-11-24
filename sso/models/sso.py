# coding=utf8

"""
Copyright 2015 SSO Project
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy import Integer, String, Column, TEXT
from . import ModelBase, Session
from ..exceptions import Error


class User(ModelBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(45), nullable=True)
    username = Column(String(45))
    password = Column(String(200))

    @classmethod
    def login(cls, username, password):
        user = Session().query(cls).filter(cls.username == username).first()
        if not user:
            raise Error(Error.USER_NOT_FOUND)
        if user.password != password:
            raise Error(Error.USER_OR_PASS_ERROR)
        return user

    @classmethod
    def register(cls, user_data):
        user = cls(**user_data)
        session = Session()
        session.add(user)
        try:
            session.commit()
        except IntegrityError as e:
            if e.orig[0] == 1062:
                raise Error(Error.USER_EXISTED)
        return user

    @classmethod
    def get(cls, uid):
        return Session().query(User).get(uid)


class Profile(ModelBase):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)