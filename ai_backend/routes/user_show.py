from flask import Blueprint, jsonify
from models.user import User
usershow_bp = Blueprint("usershow", __name__)

@usershow_bp.route("/users/allusers", methods=["GET"])
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
            "created_at": user.created_at
        })

    return jsonify({
        "count": len(output),
        "users": output
    }), 200