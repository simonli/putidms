# -*- coding:utf-8 -*-
from flask_script import Manager, Server
from putidms import create_app

manager = Manager(create_app('../config.py'))

manager.add_command("runserver", Server('localhost', port=5000))

if __name__ == "__main__":
    manager.run()
