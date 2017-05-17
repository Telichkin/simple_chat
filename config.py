import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    DATABASE_URI = 'sqlite://'

