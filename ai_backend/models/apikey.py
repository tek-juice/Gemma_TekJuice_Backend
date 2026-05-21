from config.services.extensions import db
from datetime import datetime
import secrets

class Projects(db.Model):
    __tablename__= "projects"

    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, defaulte=datetime.utcnow, onupdate = datetime)

    #relationship
    apis = db.relationship("ApiKey", backref="project", lazy=True, cascade="all, delete-orphan")


class ApiKey(db.Model):
    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Column,db.String(100), unique=True, nullable=False)
    key = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship
    user = db.relationship("User", back_populates="api_keys")

    def __init__(self, user_id):
        self.user_id = user_id
        self.key = self.generate_key()

    @staticmethod
    def generate_key():
        return "tj_" + secrets.token_hex(32)