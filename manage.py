# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gevent import monkey
monkey.patch_all()  # NOQA

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from instub.app import app


manager = Manager(app)
manager.add_command("run", Server(host='127.0.0.1',
                                  port=5010, use_reloader=True))
manager.add_command("shell", Shell())
manager.add_command('db', MigrateCommand)

manager.run()
