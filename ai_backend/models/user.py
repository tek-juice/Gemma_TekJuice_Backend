from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.string(255), nullable=False)
    role = db.Column(db.String(50), default="user") #admin or user
    created_at = db.Column(db.Datetime, default=datetime.utcnow)

    def is_admin(self):
        return self.role == "admin"