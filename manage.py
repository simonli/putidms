# -*- coding:utf-8 -*-
from flask_script import Manager, Server, Shell

from putidms import create_app
from putidms.extensions import db
from putidms.models.org import Duty
from putidms.models.user import Role, User

app = create_app('default')

manager = Manager(app)

@manager.option('-u', '--username', dest='username')
@manager.option('-r', '--realname', dest='realname')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
@manager.option('-role', '--role_id', dest='role_id')
@manager.option('-div', '--division_id', dest='division_id')
def create_admin(username,password,realname,email,role_id,division_id):
    username = ''


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,Duty=Duty)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command("runserver", Server('localhost', port=5000))

if __name__ == "__main__":
    manager.run()
