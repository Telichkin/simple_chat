from flask_jwt_extended import tokens
from flask_jwt_extended.config import config
from jwt.exceptions import DecodeError, ExpiredSignatureError


def get_username_from_token(token):
    try:
        username = tokens.decode_jwt(token, config.decode_key, config.algorithm, csrf=False)["identity"]
    except (DecodeError, ExpiredSignatureError):
        username = None
    return username
