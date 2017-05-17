from flask import Flask


def create(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from .simple_chat import root
    app.register_blueprint(root)

    return app
