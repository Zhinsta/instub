# coding: utf-8

from flask import views
from flask import request
from flask import render_template
from flask import current_app
from flask.ext.login import login_required, current_user

from instub.models import User
from instub.pager import Pager


class Home(views.MethodView):

    template = '/panel/users.html'

    @login_required
    def get(self):
        query = User.query
        pager = Pager(query.count())
        users = (query.order_by(User.created_time)
                 .offset(pager.offset)
                 .limit(pager.per_page)
                 .all())
        return render_template(self.template, users=users, pager=pager)
