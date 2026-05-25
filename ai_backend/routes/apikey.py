from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.apikey import ApiKey, Projects
from config.services.extensions import db
from models.user import User
import secrets

api_key_bp = Blueprint("api_key", __name__)

@api_key_bp.route("/key/create", methods=["POST"])
@jwt_required()
def create_api_key():
    """
    Create API key under a project
    ---
    tags:
      - API Keys
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - project_id
          properties:
            project_id:
              type: integer
              example: 1
    responses:
      201:
        description: API key created successfully
      400:
        description: Missing or invalid project
      404:
        description: Project not found
    """

    user_id = get_jwt_identity()

    data = request.get_json()
    project_id = data.get("project_id")

    user_projects = Projects.query.filter_by(user_id=user_id).all()

    if not user_projects:
        return jsonify({
            "error": "No projects found. Please create a project first"
        }), 400
    
    if not project_id:
        return jsonify({
            "error": "project_id is required"
        }), 400
    
    project = Projects.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({
            "error": "Project not found or not owned by user"
        }), 404


    api_key = ApiKey(user_id=user_id, project_id = project.id)

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "message": "API key created succefully",
        "api_key": api_key.key,
        "project": {
          "id": project.id,
          "name": project.name,
          "description": project.description,
          "user_id": project.user_id
        }
    }), 201


@api_key_bp.route("/key/user", methods=["GET"])
@jwt_required()
def get_api_keys_by_user():
    """
    Get API keys by user ID
    ---
    tags:
      - API Keys
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
                "created_at": key.created_at,
                "project_id": key.project_id
            }
            for key in api_keys
        ]
    }), 200