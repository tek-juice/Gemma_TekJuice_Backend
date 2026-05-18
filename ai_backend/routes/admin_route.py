from flask import Blueprint, request, jsonify
from models.admin import db, Admin
from werkzeug.security import generate_password_hash
from helpers.admin_user import admin_required, preserve_docs
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
import re
from models.user import User

admin_bp = Blueprint("admin",__name__)
@admin_bp.route("/register", methods=["POST"])
def register_admin():
    """
      Create Admin User
      ---
      tags:
        - Admin

      operationId: register_admin

      consumes:
        - application/json

      security:
        - Bearer: []

      parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            required:
              - name
              - email
              - password
            properties:
              name:
                type: string
                example: John Admin
              email:
                type: string
                example: admin@example.com
              password:
                type: string
                example: strongpassword123

      responses:
        201:
          description: Admin created successfully
          schema:
            type: object
            properties:
              message:
                type: string
                example: Admin Created successfully

        400:
          description: Validation error or missing fields

        401:
          description: Unauthorized (missing or invalid token)

        403:
          description: Forbidden (not an admin)

        500:
          description: Server error
      """
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not name:
            return jsonify({"error": "Name required"}), 400
        
        if not email:
            return jsonify({"error": "Email required"}), 400
        
        if not password:
            return jsonify({"error": "Password required"}), 400
        
        if not re.match(email_pattern, email):
            return jsonify({"error": "Invalid email format"}), 400
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({"error": "User already exists"}), 400
        
        hashed_password = generate_password_hash(password)

        admin = User(
            name =  name,
            email = email,
            password = hashed_password, 
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        return jsonify({
            "message": "Admin Created succefully"
        }), 201
    
    except Exception as e:
        return jsonify({
            "error": "something went wrong",
            "details": str(e)
        }),500

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    """
      Admin Login
      ---
      tags:
        - Admin
      parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
                example: admin@example.com
              password:
                type: string
                example: strongpassword123

      responses:
        200:
          description: Login successful
        401:
          description: Invalid credentials
        403:
          description: Not an admin
    """
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "email and password required"}), 400
        
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error", "Invalid credentiasl"}), 401
        
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if user.role != "admin":
            return jsonify({"error", "Access denied: Not admin"}), 403
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return jsonify({
            "message": "Admin login successful",
            "token": access_token,
            "admin": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Something went wrong",
            "details": str(e)
        }), 500
