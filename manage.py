# -*- coding:utf-8 -*-
from flask_script import Manager, Server
from putidms import create_app
from putidms.extensions import db

app = create_app('../config.py')

manager = Manager(app)

manager.add_command("runserver", Server('localhost', port=5000))


@manager.command
def create_all():
    db.create_all(app=app)

if __name__ == "__main__":
    manager.run()
