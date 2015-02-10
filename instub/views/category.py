# coding: utf-8

from flask import views
from flask import render_template

from instub.models import User


class HomeView(views.MethodView):
    def get(self):
        user = User.query.all()
        return render_template('home.html')



class Welcome(views.MethodView):

    def get(self):
        return render_template('welcome.html')
