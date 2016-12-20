# -*- coding:utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = True
    SECRET_KEY = '\xb33]\xdbO\xb4k\x8fU\x00ZQ\xac\x83\x89Y)\x01\x10\xfa\x06\xa8\x80\x8e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///putidms.db'
    # SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:cncode@localhost:5432/putidms"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # WTF_CSRF_ENABLED = False
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
