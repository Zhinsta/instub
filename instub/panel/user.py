# coding: utf-8

from flask import views
from flask import request


class User(views.MethodView):

    def get(self):
        query = User.query
        return 'hello instub panel!'
