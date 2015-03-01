# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask
from werkzeug.utils import import_string
from .database import db, migrate

from instub.utils import login_manager, online_user, all_categories
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


def register_blueprint(app):
    blueprint_list = ['instub.views.blueprint',
                      'instub.views.user_blueprint',
                      'instub.views.category_blueprint']
    for blueprint in blueprint_list:
        app.register_blueprint(import_string(blueprint))
    return app


def register_jinja_funcs(app):
    funcs = dict(
        online_user=online_user,
        all_categories=all_categories
    )
    app.jinja_env.globals.update(funcs)
    return app

register_blueprint(app)
register_jinja_funcs(app)
register_errorhandlers(app)
