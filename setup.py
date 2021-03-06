# coding: utf-8

from setuptools import setup, find_packages

install_requires = [
    'Flask-Cache',
    'MySQL-python',
    'flask',
    'sqlalchemy',
    'wtforms==1.0.5',
    'flask-admin',
    'flask-restful',
    'jsonschema',
    'flask-sqlalchemy',
    'flask-migrate',
    'flask-wtf',
    'flask-login',
    'gevent',
    'itsdangerous',
    'python-instagram',
    'pymysql',
    'redis',
]

entry_points = {
    'console_scripts': [
        'run = instub.runserver:main',
    ]
}

setup(
    name="instub",
    version="0.0.1",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points,
)
