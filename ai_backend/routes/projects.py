from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from config.services.extensions import db
from models.apikey import Projects
from models.user import User
from models.apikey import ApiKey

project_bp = Blueprint("project_bp", __name__)

@project_bp.route("/projects", methods=["POST"])
@jwt_required()
def create_project():
    """
Create a new project
---
tags:
  - Projects
security:
  - Bearer: []
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          example: AI Chat System
        description:
          type: string
          example: Handles chatbot workflows
responses:
  201:
    description: Project created successfully
    schema:
      type: object
      properties:
        message:
          type: string
          example: Project created successfully
  400:
    description: Validation error
  404:
    description: User not found
"""
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Project name is required"}), 400
    
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error", "User not found"}), 400
    
    project  = Projects(
        name=name,
        description=description,
        user_id=user_id
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "message": "Project created succefully"
    }), 201

@project_bp.route("/project/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    """
Delete a project (and all API keys under it)
---
tags:
  - Projects
security:
  - Bearer: []
parameters:
  - name: project_id
    in: path
    required: true
    type: integer
  - name: confirm
    in: query
    required: false
    type: boolean
    description: Must be true to confirm deletion
responses:
  200:
    description: Project deleted successfully
  400:
    description: Confirmation required
  404:
    description: Project not found
  403:
    description: Unauthorized
"""
    user_id = get_jwt_identity()

    project = Projects.query.filter_by(
        id=project_id,
        user_id = user_id,
        is_deleted = False
    ).first()

    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    confirm = request.args.get("confirm", "false").lower()

    if confirm != "true":
        return jsonify({
            "warning": "Deleting this project will also delete all API keys under it",
            "message": "Add ?confirm=true to confirm deletion."
        }), 400
    
    project.is_deleted = True

    for api_key in project.apis:
        if not api_key.is_deleted:
          api_key.is_deleted = True
          api_key.is_active = False

    db.session.commit()

    return jsonify({
        "message": "Project and all associated API keys deleted successfully"
    }), 200

@project_bp.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():
    """
    Get all projects belonging to the logged-in user
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    responses:
      200:
        description: List of user projects
        schema:
          type: object
          properties:
            projects:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  created_at:
                    type: string
    """

    current_user_id = get_jwt_identity()

    projects = Projects.query.filter_by(user_id=current_user_id, is_deleted = False).all()

    if not projects:
        return jsonify({
            "error": "You don't have any projects created",
            "user_id": current_user_id
        }), 404
    
    return jsonify({
        "user_id": current_user_id,
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "user_id": p.user_id,
                "created_at": p.created_at,
            }
            for p in projects
        ]
    }), 200