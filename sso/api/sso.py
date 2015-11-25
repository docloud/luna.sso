# coding=utf8

"""
Copyright 2015 Luna Project
"""

from werkzeug.security import gen_salt
from flask import make_response, jsonify
from webargs import fields
from luna import cache, View
from luna.models import serialize
from luna.decorators import route, use_args, use_kwargs
from ..models.sso import User
from ..exceptions import Error


class Sso(View):
    router = "/sso"

    def _login(self, **kwargs):
        user = User.login(**kwargs)
        token = gen_salt(32)
        cache.set(token, user.id, timeout=7200)
        return user, token

    login_args = {
        "username": fields.Str(required=True),
        "password": fields.Str(required=True),
    }

    @route("login", methods=("POST",))
    @use_args(login_args)
    def login(self, args):
        user, token = self._login(**args)
        resp = make_response(jsonify({"token": token}))
        resp.headers["Authorization"] = token
        resp.set_cookie("Authorization", token)
        return resp

    register_args = login_args

    @route("register", methods=("POST",))
    @use_args(register_args)
    def register(self, args):
        user = User.register(args)
        _, token = self._login(username=user.username,
                               password=user.password)
        resp = make_response(jsonify({"token": token}))
        resp.headers["Authorization"] = token
        resp.set_cookie("Authorization", token)
        return resp

    @route("user")
    @use_kwargs({
        'token': fields.Str(required=True, load_from="Authorization",
                            location="headers"),
    })
    def get_user(self, token):
        uid = cache.get(token)
        if not uid:
            raise Error(Error.TOKEN_INVALID)
        user_data = serialize(User.get(uid) or User())
        user_data.pop("password")
        return user_data
