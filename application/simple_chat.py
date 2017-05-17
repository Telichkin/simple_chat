from flask import Blueprint, request, jsonify

from application import db
from application.models import User


root = Blueprint("root", __name__)


@root.route("/users/", methods=["POST"])
def create_user():
    user_data = request.get_json()

    password = user_data.get("password", None)
    if not password:
        return jsonify({"error": "Password is needed"}), 400

    username = user_data.get("username", None)
    if not username:
        return jsonify({"error": "Username is needed"}), 400

    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"token": ""}), 201
