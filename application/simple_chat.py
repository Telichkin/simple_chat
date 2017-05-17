from flask import Blueprint, request

from application import db
from application.models import User


root = Blueprint("root", __name__)


@root.route("/users/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    username = user_data.get("username", None)
    password = user_data.get("password", None)

    if not password:
        return "Password is needed", 400

    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return "OK", 201
