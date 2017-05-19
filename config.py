import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_CLASS = "redis.StrictRedis"
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
    SOCKETIO_MESSAGE_QUEUE = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "development"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    SOCKETIO_MESSAGE_QUEUE = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SECRET_KEY = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    REDIS_CLASS = "mockredis.mock_strict_redis_client"
