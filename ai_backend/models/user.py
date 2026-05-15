from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config.services.extensions import db



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(255), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # relationship
    api_keys = db.relationship("ApiKey", back_populates="user", lazy=True)

class EmailVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship("User", backref="verifications")

