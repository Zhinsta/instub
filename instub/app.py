# coding: utf-8

import os

from flask import Flask

from instub import views

app = Flask(__name__)

app.config.from_pyfile(os.path.join('config.py'))
app.register_blueprint(views.blueprint)
