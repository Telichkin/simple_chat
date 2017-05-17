from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    from .simple_chat import root
    app.register_blueprint(root)

    return app
