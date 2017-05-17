from flask import Blueprint


root = Blueprint('root', __name__)


@root.route('/')
def hello_world():
    return 'Hello World!'
