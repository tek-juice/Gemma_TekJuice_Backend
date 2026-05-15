from flask import Blueprint, jsonify
from models.apikey import ApiKey
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

api_key_fetch_bp = Blueprint("api_key_fetch", __name__)

@api_key_fetch_bp.route("/key/user", methods=["GET"])
@jwt_required()
def get_api_keys_by_user():
    """
    Get API keys by user ID
    ---
    tags:
      - API keys
    security:
      - Bearer: []
    responses:
      200:
        description: API keys retrieved successfully
      404:
        description: User not found or no API keys
    """
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    api_keys = ApiKey.query.filter_by(user_id=current_user_id).all()

    if not api_keys:
        return jsonify({
            "message": "No API keys found for this user",
            "user_id": current_user_id
        }), 404

    return jsonify({
        "user_id": current_user_id,
        "api_keys": [
            {
                "id": key.id,
                "key": key.key,
                "is_active": key.is_active,
                "created_at": key.created_at
            }
            for key in api_keys
        ]
    }), 200