# coding: utf-8

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/instub?charset=utf8'
SECRET_KEY = 'Instub'

try:
    from instab.config_local import *  # NOQA
except ImportError:
    pass
