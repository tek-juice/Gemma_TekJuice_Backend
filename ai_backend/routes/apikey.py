from flask import Blueprint, request, jsonify
from models.apikey import ApiKey
from config.services.extensions import db
from models.user import User

api_key_create_bp = Blueprint("api_key", __name__)

@api_key_create_bp.route("/key/create", methods=["POST"])
def create_api_key():
    """
    Create API key
    ---
    tags:
      - API keys
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: integer
              example: 1
    responses:
      201:
        description: API key created
    """

    data = request.get_json() or {}
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    api_key = ApiKey(user_id=user_id)

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "message": "API key created successfully",
        "api_key": api_key.key 
    }), 201