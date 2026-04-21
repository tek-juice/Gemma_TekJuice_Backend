from flask import Blueprint, request, jsonify
from  models.user import User
from config.services.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/register", methods=["POST"])
def register_user():
    """
    Register a new user
    ---
    tags:
      - User
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
              example: user@example.com
            password:
              type: string
              example: secret123
    responses:
      201:
        description: User created successfully
      400:
        description: Missing fields or user exists
    """
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)

    user = User(
        email = email,
        password = hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created succefully"}), 201


@user_bp.route("/user/login", methods=["POST"])
def login_user():
    """
    User login
    ---
    tags:
      - User
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
              example: user@example.com
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
        return jsonify({"error": "Email and password required"}), 400
    
    user =User.query.filter_by(email = email).first()
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({
      "message": "Login successful",
      "user_id": user.id,
      "token": "some-jwt-token-here"
    }), 200
        

