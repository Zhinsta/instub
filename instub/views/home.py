# coding: utf-8

from flask import views
from flask import request

from instub.models import User

class HomeView(views.MethodView):
    def get(self):
        user = User.query.all()
        print user
        return 'hello instub!'
