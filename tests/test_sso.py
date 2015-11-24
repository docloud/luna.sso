# coding=utf8

"""
Copyright 2015 Luna Project
"""

from . import Data
from luna.clients import http

sso = Data()
sso.success = [
    {
        "username": "demo",
        "password": "1234"
    }
]

def test_login_01():
    http.get('sso/login', json=sso.success[0])