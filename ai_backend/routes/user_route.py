from flask import Blueprint, request, jsonify
from  models.user import User
from config.services.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import re
import random
from datetime import datetime, timedelta
from models.user import EmailVerification

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
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: John Doe
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
    try:
      data = request.get_json()

      name = data.get("name")
      email = data.get("email")
      password = data.get("password")

      email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

      if not email:
          return jsonify({"error": "Email is required,"}), 400
      if not password:
          return jsonify({"error": "Password is required"}), 400
      if not name:
          return jsonify({"error": "Name is required"}), 400
      if not re.match(email_pattern, email):
          return jsonify({"error": "Invalid email formart"}), 400
      
      existing_user = User.query.filter_by(email=email).first()
      if existing_user:
          return jsonify({"error": "User already exists"}), 400
      
      hashed_password = generate_password_hash(password)

      user = User(
          name = name,
          email = email,
          password = hashed_password
      )

      db.session.add(user)
      db.session.commit()

      code = str(random.randint(100000, 999999))

      # store in the verification table 
      verification = EmailVerification(
         user_id = user.id,
         code = code,
         expires_at=datetime.utcnow() + timedelta(minutes=10)
      )

      db.session.add(verification)
      db.session.commit()

      return jsonify({"message": "User created succefully"}), 201
    
    except Exception as e:
      return jsonify({
          "error": "Something went wrong, Please contact support",
          "details": str(e)
      }), 500
    


@user_bp.route("/user/verify-email", methods=["POST"])
def verify_email():
    """
      Verify user email
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
              - code
            properties:
              email:
                type: string
                example: user@example.com
              code:
                type: string
                example: 483920

      responses:
        200:
          description: Email verified successfully

        400:
          description: Invalid code or missing fields

        404:
          description: User not found
    """

    try:
      data = request.get_json()

      email = data.get("email")
      code = data.get("code")

      if not email or not code:
        return jsonify({"error": "Email and code reqiured"}), 400
      
      # find user 
      user = User.query.filter_by(email=email).first()

      if not user:
        return jsonify({"error": "Your email is not registered, please register"}), 404
      
      # find the verification code 
      verification = EmailVerification.query.filter_by(user_id=user.id).first()

      if not verification:
         return jsonify({"error": "Verification record not found"}), 404

      # compare code 
      if verification.code != code:
        return jsonify({"error": "Invalid verification code"})
      
      # check expiry

      if verification.expires_at < datetime.utcnow():
         return jsonify({
            "error": "Verification code expired"
         }), 400
      
      # verify email 
      user.is_email_verified = True
      db.session.delete(verification)

      db.session.commit()

      return jsonify({
         "message:" "Email verified successfully"
      }), 200

    except Exception as e:
       return jsonify({
          "error": "Something went wrong contact support",
          "details": str(e)
       }), 500

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

    # name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user =User.query.filter_by(email = email).first()
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
      "message": "Login successful",
      "user_id": user.id,
      "token": access_token,
      "email": user.email,
      "name": user.name
    }), 200
        

