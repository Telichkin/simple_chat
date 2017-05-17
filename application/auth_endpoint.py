from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from application.models import User


auth_endpoint = Blueprint("auth_endpoint", __name__, url_prefix="/auth")


@auth_endpoint.route("/", methods=["POST"])
def token_auth():
    auth_data = request.get_json()

    username = auth_data.get("username", None)
    if not username:
        return jsonify({"error": "Username is needed"}), 400

    password = auth_data.get("password", None)
    if not password:
        return jsonify({"error": "Password is needed"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.is_password_valid(password):
        return jsonify({"error": "Incorrect username or password"}), 400

    return jsonify({"token": create_access_token(identity=username)}), 200
