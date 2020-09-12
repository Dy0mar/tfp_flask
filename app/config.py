# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))

env = os.path.join(basedir, '.env')
load_dotenv(find_dotenv(filename=env))


class BaseConfig(object):
    FLASK_DEBUG = False

    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # generate test data
    GENERATE = bool(int(os.environ.get('GENERATE', 0)))
    GENERATE_TEST_ROWS = int(os.environ.get('GENERATE_TEST_ROWS', 0))

    # Pagination
    DEFAULT_PER_PAGE = int(os.environ.get('DEFAULT_PER_PAGE', 0))

    # security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT)')
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    BASE_URL = os.environ.get('BASE_URL')


class DevelopmentConfig(BaseConfig):
    def __init__(self, *args, **kwargs):
        self.FLASK_DEBUG = True
        self.DEBUG = True
        super().__init__(*args, **kwargs)


class ProductionConfig(BaseConfig):
    def __init__(self, *args, **kwargs):
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            self.SQLALCHEMY_DATABASE_URI = db_url

        super().__init__(*args, **kwargs)
