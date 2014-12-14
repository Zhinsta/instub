# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask
from .database import db, migrate

from instub import views
from instub import panel

from instub.utils import login_manager

app = Flask(__name__)

app.config.from_pyfile(os.path.join('config.py'))

db.init_app(app)
migrate.init_app(app, db)

login_manager.init_app(app)
login_manager.login_view = "panel.login"

app.register_blueprint(views.blueprint)
app.register_blueprint(panel.blueprint)
