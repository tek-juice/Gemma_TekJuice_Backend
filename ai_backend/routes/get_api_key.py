from flask import Blueprint, jsonify
from models.apikey import ApiKey
from models.user import User

api_key_fetch_bp = Blueprint("api_key_fetch", __name__)

@api_key_fetch_bp.route("/key/user/<int:user_id>", methods=["GET"])
def get_api_keys_by_user(user_id):
    """
    Get API keys by user ID
    ---
    tags:
      - API keys
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID of the user
        example: 1

    responses:
      200:
        description: API keys retrieved successfully
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 1
            api_keys:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  key:
                    type: string
                    example: tj_abc123...
                  is_active:
                    type: boolean
                    example: true
                  created_at:
                    type: string
                    example: 2026-04-22T10:00:00

      404:
        description: User not found or no API keys
    """

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    api_keys = ApiKey.query.filter_by(user_id=user_id).all()

    if not api_keys:
        return jsonify({
            "message": "No API keys found for this user",
            "user_id": user_id
        }), 404

    return jsonify({
        "user_id": user_id,
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