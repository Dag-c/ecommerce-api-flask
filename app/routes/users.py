from flask import Blueprint, request, jsonify
from app.models import User
from app.database import db
from app.services.auth import encrypt_password, token_required
from app.utils.exceptions import *

# Create a Blueprint for users
users_bp = Blueprint('users', __name__)


# Create a new user (POST)
@users_bp.route('/users', methods=['POST'])
def create_user():
    """
        Create a new user
        ---
        tags:
          - Users
        summary: Creates a new user account
        description: Endpoint to register a new user with name, email, and password.
        parameters:
          - in: body
            name: body
            required: true
            description: JSON object containing user details
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
                  example: john.doe@example.com
                password:
                  type: string
                  format: password
                  example: "securepassword123"
                role:
                  type: string
                  enum: [buyer, seller, admin]
                  example: buyer
        responses:
          201:
            description: User created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User created
                user:
                  type: integer
                  example: 1
          400:
            description: Bad request (missing data or invalid input)
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "data is missing"
          500:
            description: Unexpected server error
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "An unexpected error occurred"
                details:
                  type: string
                  example: "Database connection error"
        """
    data = request.get_json()

    # Ensure that the data requirement is present
    if not data.get('name') or not data.get('email') or not data.get('password'):
        raise BadRequestsError("Missing required fields: name, email, or password")
    if User.query.filter_by(email=data['email']).first():
        raise BadRequestsError("Email already registered")

    hashed_password = encrypt_password(data['password'])
    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'buyer')  # Default role 'user'
    )

    # Store new user in database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created", "user": new_user.id}), 201


# Get a user by ID (GET)
@users_bp.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(id: int):
    """
    Get user by ID
    ---
    security:
      - BearerAuth: []
    tags:
      - Users
    summary: Retrieve a user by their unique ID
    description: Endpoint to retrieve a user's data by their unique ID.
    parameters:
      - in: path
        name: id
        required: true
        description: The unique ID of the user to retrieve
        schema:
          type: integer
          example: 123
      - in: header
        name: Authorization
        required: true
        description: JWT token for authentication
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
    responses:
      200:
        description: User data successfully retrieved
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 123
                name:
                  type: string
                  example: "John Doe"
                email:
                  type: string
                  example: "john.doe@example.com"
                role:
                  type: string
                  example: "buyer"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-03-24T14:30:00Z"
      401:
        description: Unauthorized – Invalid or expired token
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Invalid token!"
                message:
                  type: string
                  example: "Please provide a valid JWT token"
      404:
        description: User not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "User not found"
      429:
        description: Too many requests – Rate limit exceeded
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Too many requests"
                message:
                  type: string
                  example: "You have exceeded the allowed rate limit. Try again later."
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "An unexpected error occurred"
                details:
                  type: string
                  example: "Database connection error"
    """

    user = User.query.get(id)
    if not user:
        raise ResourceNotFound("User not found")

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.name,
        "created_at": user.created_at
    }), 200


# Get a user all users
@users_bp.route('/users', methods=['GET'])
@token_required
def get_all_users():
    """
        Get all users
        ---
        security:
          - BearerAuth: []
        tags:
          - Users
        summary: Retrieve all users
        description: Endpoint to retrieve a list of all users in the system. The request must be authenticated with a JWT token.
        parameters:
          - in: header
            name: Authorization
            required: true
            description: "JWT token for authentication"
            schema:
              type: string
              example: "Bearer your_jwt_token_here"
        responses:
          200:
            description: Successfully retrieved the list of users
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: "John Doe"
                      email:
                        type: string
                        example: "john.doe@example.com"
                      role:
                        type: string
                        example: "buyer"
                      created_at:
                        type: string
                        format: date-time
                        example: "Sun, 16 Mar 2025 17:28:23 GMT"
          404:
            description: No users found
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Not users found"
          401:
            description: Unauthorized – Invalid or expired token
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Invalid token!"
                    message:
                      type: string
                      example: "Please provide a valid JWT token"
          500:
            description: Internal server error
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "An unexpected error occurred"
                    details:
                      type: string
                      example: "Database connection error"

    """

    users = User.query.order_by(User.id).all()
    if not users:
        raise ResourceNotFound("No users found")

    # turn the list of objects to a dictionary list
    users_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.name,
            "created_at": user.created_at
        }
        for user in users
    ]

    return jsonify(users_list), 200


@users_bp.route('/users/<int:user_id>', methods=['PATCH'])
@token_required
def update_user(user_id: int):
    """
        Update user details.
        ---
        security:
          - BearerAuth: []
        tags:
          - Users
        parameters:
          - in: header
            name: Authorization
            required: true
            description: "JWT token for authentication"
            schema:
              type: string
              example: "Bearer your_jwt_token_here"
          - name: user_id
            in: path
            type: integer
            required: true
            description: ID of the user to be updated
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The name of the user.
                email:
                  type: string
                  description: The email address of the user.
                password:
                  type: string
                  description: The password of the user.
                role:
                  type: string
                  description: The role of the user (e.g., "buyer", "seller").
              example:
                name: "Juan Pérez"
                email: "juan.perez@example.com"
                password: "newpassword123"
                role: "buyer"
        responses:
          200:
            description: User updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User updated successfully"
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Juan Pérez"
                    email:
                      type: string
                      example: "juan.perez@example.com"
                    role:
                      type: string
                      example: "buyer"
          400:
            description: Bad request, invalid input or parameters
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "User not found"
          401:
            description: Unauthorized, invalid or missing token
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Token is missing or invalid"
        """

    data = request.get_json()
    user = db.session.get(User, user_id)

    if not user:
        raise ResourceNotFound("User not found")

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = encrypt_password(data['password'])
    if 'role' in data:
        if data['role'] not in ['buyer', 'seller', 'admin']:
            raise BadRequestsError("Invalid role, valid roles are: buyer, seller, admin")
        user.role = data['role']

    # Save the changes in database
    db.session.commit()

    # Response
    return jsonify({
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.name
        }
    }), 200


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id: int):
    """
       Delete a user by ID.
       ---
       security:
         - BearerAuth: []
       tags:
         - Users
       parameters:
         - in: header
           name: Authorization
           required: true
           description: "JWT token for authentication"
           schema:
             type: string
             example: "Bearer your_jwt_token_here"
         - in: path
           name: user_id
           required: true
           description: ID of the user to be deleted
           schema:
             type: integer
             example: 1
       responses:
         200:
           description: User deleted successfully
           schema:
             type: object
             properties:
               message:
                 type: string
                 example: "User deleted successfully"
         404:
           description: User not found
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "User not found"
         401:
           description: Unauthorized, invalid or missing token
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "Token is missing or invalid"
       """
    user = db.session.get(User, user_id)

    if not user:
        raise ResourceNotFound("User not found")

    # Delete user
    db.session.delete(user)
    db.session.commit()

    # Response
    return jsonify({"message": "User delete successfully"}), 200
