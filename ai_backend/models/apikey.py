from config.services.extensions import db
from datetime import datetime
import secrets

class Projects(db.Model):
    __tablename__= "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate = datetime.utcnow)

    apis = db.relationship("ApiKey", backref="project", lazy=True)



class ApiKey(db.Model):
    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey("projects.id"), nullable=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship
    user = db.relationship("User", back_populates="api_keys")

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
        self.key = self.generate_key()

    @staticmethod
    def generate_key():
        return "tj_" + secrets.token_hex(32)
    
# class Tokens(db.Model):
#     __tablename__= "tokens"

#     id  = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     project_id = db.Column(db.Integer, db.ForeignKey("key"), nullable=False)
#     key = db.column(db.Integer, db.ForeignKey("key", nallable=False))
#     total_tokens = db.Column(db.Integer, default=0)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
# class Billing(db.Model):
#     __tablename__= "billing"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
#     project_id = db.Column(db.Integer, db.ForeignKey("project_id"), nullable=False)
#     key = db.Column(db.Integer, db.ForeignKey("key"), nullable=False)
#     amount = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)





