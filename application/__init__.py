from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()
socket_io = SocketIO()


def create(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    socket_io.init_app(app)

    from .simple_chat import root
    app.register_blueprint(root)

    return app
