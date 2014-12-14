# coding: utf-8

from md5 import md5

from flask import request
from flask import flash
from flask import views
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import render_template

from flask.ext.login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, AddAdminForm
from instub.models import User


class Login(views.MethodView):

    template = '/panel/login.html'

    def get(self):
        if current_user.is_authenticated():
            return redirect(url_for('panel.index'))
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            # login and validate the user...
            email = form.email.data
            password = form.password.data
            password = md5('instub%s' % password).hexdigest()
            user = (User.query
                    .filter(User.email == email)
                    .filter(User.password == password)
                    .first())
            if not user:
                return render_template("login.html", form=form)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("panel.index"))
        return render_template(self.template, form=form)


class Logout(views.MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('panel.login'))


class AddAdmin(views.MethodView):

    template = '/panel/add_admin.html'

    @login_required
    def get(self):
        form = AddAdminForm()
        return render_template(self.template, form=form)

    @login_required
    def post(self):
        form = AddAdminForm()
        if form.validate_on_submit():
            password = md5('instub%s' % form.password.data).hexdigest()
            user = User.create(name=form.name.data,
                               email=form.email.data,
                               mobile=form.mobile.data,
                               password=password)
            return redirect(request.args.get("next") or url_for("panel.index"))
        return render_template(self.template, form=form)
