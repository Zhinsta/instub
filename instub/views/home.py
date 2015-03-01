# coding: utf-8

from flask import views
from flask import render_template

from instub.models import User, Category


class HomeView(views.MethodView):
    def get(self):
        categories = Category.query.order_by(Category.sort_score.desc()).all()
        return render_template('home.html', categories=categories)



class Welcome(views.MethodView):

	def get(self):
		return render_template('welcome.html')
