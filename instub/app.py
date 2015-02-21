# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask
from .database import db, migrate

from instub import views

from instub.utils import login_manager
from instub.panel import iadmin
from instub.models import iAdmin
from instub.errors import register_errorhandlers

app = Flask(__name__)

app.config.from_pyfile(os.path.join('settings.py'))

db.init_app(app)
migrate.init_app(app, db)


def init_login():
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return iAdmin.query.get(id)

init_login()

iadmin.init_app(app)

app.register_blueprint(views.blueprint)
app.register_blueprint(views.user_blueprint)
register_errorhandlers(app)

