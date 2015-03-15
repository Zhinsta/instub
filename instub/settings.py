# coding: utf-8

DEBUG = True

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_DATEBASE = 'instub'
DB_PASSWORD = ''

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:@%s:%s/%s?charset=utf8' % (
    DB_USER, DB_HOST, DB_PORT, DB_DATEBASE)
SECRET_KEY = 'Instub'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = '1'

REDIS_URL = 'redis://%s:%s/%s' % (
    REDIS_HOST, REDIS_PORT, REDIS_DB
)

INSTAGRAM_CLIENT_ID = '30fc02241ccb410fbf7fe5508c650c78'
INSTAGRAM_CLIENT_SECRET = '28ede58b51f94de594b3af4b3fff1a1f'
INSTAGRAM_REDIRECT_URI = 'http://www.dev.zhinsta.com:5000/instagram/redirect/'
INSTAGRAM_SCOPE = ['comments', 'relationships', 'likes']

try:
    from instab.config_local import *  # NOQA
except ImportError:
    pass
