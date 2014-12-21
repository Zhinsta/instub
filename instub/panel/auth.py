# coding: utf-8

from md5 import md5

from flask import request
from flask import flash
from flask import views
from flask import redirect
from flask import url_for
from flask import render_template

from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user

from .forms import LoginForm, AddAdminForm, EditAdminForm
from instub.models import Admin
from instub.utils import notfound


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
            admin = (Admin.query
                     .filter(Admin.email == email)
                     .filter(Admin.password == password)
                     .first())
            if not admin:
                return render_template("login.html", form=form)
            login_user(admin)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("panel.index"))
        return render_template(self.template, form=form)


class Logout(views.MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('panel.login'))


class AdminEdit(views.MethodView):

    template = '/panel/add_admin.html'

    @login_required
    def get(self, id=None):
        if id:
            admin = Admin.query.get(id)
            if not admin:
                return notfound('admin not exists')
            form = EditAdminForm(name=admin.name,
                                 email=admin.email,
                                 mobile=admin.mobile,
                                 password=admin.password)
        else:
            form = AddAdminForm()
        return render_template(self.template, form=form)

    def update_admin(self, id):
        admin = Admin.query.get(id)
        if not admin:
            return notfound('admin not exists')
        form = EditAdminForm()
        if form.validate_on_submit():
            password = md5('instub%s' % form.password.data).hexdigest()
            admin.update(name=form.name.data,
                         email=form.email.data,
                         mobile=form.mobile.data,
                         password=password)
            return redirect(request.args.get("next") or url_for("panel.index"))
        return render_template(self.template, form=form)

    def add_admin(self):
        form = AddAdminForm()
        if form.validate_on_submit():
            password = md5('instub%s' % form.password.data).hexdigest()
            Admin.create(name=form.name.data,
                         email=form.email.data,
                         mobile=form.mobile.data,
                         password=password)
            return redirect(request.args.get("next") or url_for("panel.index"))
        return render_template(self.template, form=form)

    @login_required
    def post(self, id=None):
        if id:
            return self.update_admin(id)
        return self.add_admin()
