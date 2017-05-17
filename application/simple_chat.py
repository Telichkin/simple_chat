from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

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

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User with current username already exists"}), 400

    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"token": create_access_token(identity=username)}), 201
