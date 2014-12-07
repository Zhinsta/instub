# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask
from .database import db, migrate

from instub import views
from instub import panel

app = Flask(__name__)

app.config.from_pyfile(os.path.join('config.py'))

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(views.blueprint)
app.register_blueprint(panel.blueprint)
