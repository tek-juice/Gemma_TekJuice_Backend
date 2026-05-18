from flask import Blueprint, jsonify
from models.user import User
usershow_bp = Blueprint("usershow", __name__)
from helpers.admin_user import admin_required
from flask_jwt_extended import jwt_required

@usershow_bp.route("/users/allusers", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():
    """
    Get all users
    ---
    tags:
        - Admin
    responses:
        200:
            description: List of all users
    """

    users = User.query.all()

    output = []
    for user in users:
        output.append({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "email Verified": user.is_email_verified,
            "created_at": user.created_at
        })

    return jsonify({
        "count": len(output),
        "users": output
    }), 200