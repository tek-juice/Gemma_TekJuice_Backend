from flask import Blueprint, request, jsonify
from models.user import db, User
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("admin/register", methods=["POST"])

def register_admin():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)

    admin = User(
        email = email,
        password = hashed_password,
        role = "admin"
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin created succefully"}), 201