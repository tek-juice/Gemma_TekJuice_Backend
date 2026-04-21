from flask import Blueprint, request, jsonify
from models.admin import db, Admin
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/admin/register", methods=["POST"])

def register_admin():
    """
    Register an admin user
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
              example: secret123
    responses:
      201:
        description: Admin created successfully
      400:
        description: Missing fields or user exists
    """
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    existing_user = Admin.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)

    admin = Admin(
        email = email,
        password = hashed_password,
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin created succefully"}), 201


@admin_bp.route("admin/login", methods=["POST"])
def admin_login():
    """
    Admin login
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
              example: secret123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password reqired"}), 400
    
    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({"error": "Invalid admin credentials"}), 401
    
    return jsonify({
        "message": "Admin login succeful",
        "admin_id": admin.id
    }), 200