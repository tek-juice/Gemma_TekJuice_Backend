from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config.services.extensions import db



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship 
    api_keys = db.relationship("ApiKey", back_populates="user", lazy=True)

