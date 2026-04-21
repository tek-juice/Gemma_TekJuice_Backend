from config.services.extensions import db
from datetime import datetime
import secrets


class ApiKey(db.Model):
    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

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