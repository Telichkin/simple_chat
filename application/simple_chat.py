from flask import Blueprint, request

from application import db
from application.models import User


root = Blueprint("root", __name__)


@root.route("/users/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    user = User(
        username=user_data["username"],
        password=user_data["password"]
    )
    db.session.add(user)
    db.session.commit()
    return "OK", 201
