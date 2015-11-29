# coding=utf8

from luna.models import db, rsdb

if rsdb:
    session = rsdb.session
    ModelBase = rsdb.Model
