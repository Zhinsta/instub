# coding: utf-8

from flask import views
from flask import request


class Home(views.MethodView):
    def get(self):
        return 'hello instub panel!'
