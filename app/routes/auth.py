from flask import Blueprint, request, jsonify
from app.models import User
from app.services.auth import check_password, generate_jwt_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
        Login to get JWT token
        ---
        tags:
          - Authentication
        summary: Login to obtain a JWT token
        description: Endpoint to authenticate a user and receive a JWT token for subsequent protected requests. The user must provide a valid email and password to receive the token.
        parameters:
          - in: body
            name: body
            required: true
            description: JSON object containing user login credentials
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  example: "john.doe@example.com"
                password:
                  type: string
                  format: password
                  example: "securepassword123"
        responses:
          200:
            description: Login successful, JWT token issued
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: "Login successful"
                    token:
                      type: string
                      example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjg5MzYxNzA5LCJleHBpcmVkX2F0Ijo2MTg5NDE2Njg1fQ.Pk0h4kU4AP6zHFtrCgXzFlJhAxJ9fGzAzOg0LVLq7os"
          401:
            description: Invalid email or password
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Invalid email or password"

    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password(user, password):
        token = generate_jwt_token(user)
        return jsonify({"message": "Login successful", "token": token}), 200

    return jsonify({"error": "Invalid email or password"}), 401
