# -*- coding: utf-8 -*-

from flask import render_template
from flask.ext.login import LoginManager

login_manager = LoginManager()


def notfound(message):
    return render_template('errors.html', message=message), 404
