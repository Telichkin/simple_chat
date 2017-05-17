from werkzeug.security import generate_password_hash, check_password_hash

from application import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError("Write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_password_valid(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password):
        self.username = username
        self.password = password
