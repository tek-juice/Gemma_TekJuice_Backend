from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.apikey import ApiKey
from config.services.extensions import db
from models.user import User
import secrets

api_key_create_bp = Blueprint("api_key", __name__)

@api_key_create_bp.route("/key/create", methods=["POST"])
@jwt_required()
def create_api_key():
    """
    Create API key
    ---
    tags:
      - API keys

    security:
      - Bearer: []
    responses:
      201:
        description: API key created
    """

    user_id = get_jwt_identity()


    api_key = ApiKey(user_id=user_id)

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "message": "API key created succefully",
        "api_key": api_key.key
    }), 201