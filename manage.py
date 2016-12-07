# -*- coding:utf-8 -*-
from flask_script import Manager, Server, Shell
from putidms import create_app
from putidms.extensions import db
from putidms.models.user import Role, User
from putidms.models.org import Division, Department, Class, Duty
from putidms.models.counselor import Counselor, LeadClassRecord, EvaluationRecord, TrainingRecord

app = create_app('default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,Duty=Duty)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command("runserver", Server('localhost', port=5000))

if __name__ == "__main__":
    manager.run()
