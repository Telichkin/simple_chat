from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from application.utils import ActiveUsers


db = SQLAlchemy()
jwt = JWTManager()
socket_io = SocketIO()
active_users = ActiveUsers()


def create(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    socket_io.init_app(app)

    from .auth_endpoint import auth_endpoint
    app.register_blueprint(auth_endpoint)

    from .users_endpoint import user_endpoint
    app.register_blueprint(user_endpoint)

    from . import simple_chat

    return app
