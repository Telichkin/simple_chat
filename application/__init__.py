from flask import Flask
from flask_redis import Redis
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


redis = Redis()
db = SQLAlchemy()
jwt = JWTManager()
socket_io = SocketIO()


def create(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    redis.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    socket_io.init_app(app, async_mode="eventlet")

    from .auth_endpoint import auth_endpoint
    app.register_blueprint(auth_endpoint)

    from .users_endpoint import user_endpoint
    app.register_blueprint(user_endpoint)

    from . import chat

    return app
