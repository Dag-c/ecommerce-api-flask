from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.models import Product
from app.database import db
from app.services.auth import token_required
from app.utils.exceptions import BadRequestsError, ResourceNotFound

# Create a Blueprint for products
products_bp = Blueprint('products', __name__)


# Create a new product (POST)
@products_bp.route('/products', methods=['POST', 'OPTIONS'])
@token_required
def create_products():
    """
    Create a new product
    ---
    security:
      - BearerAuth: []
    tags:
      - Products
    summary: Creates a new product
    description: Endpoint to register a new product with seller_id, name, description, price, and stock.
    parameters:
      - in: header
        name: Authorization
        required: true
        description: JWT token for authentication
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
      - in: body
        name: body
        required: true
        description: JSON object containing product details
        schema:
          type: object
          required:
            - seller_id
            - name
            - description
            - price
            - stock
          properties:
            seller_id:
              type: integer
              example: 123
            name:
              type: string
              example: "smartphone"
            description:
              type: string
              example: "Xiaomi 13T Plus 250GB octa-core"
            price:
              type: number
              format: float
              example: 125.85
            stock:
              type: integer
              example: 35
    responses:
      201:
        description: Product created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product created"
            product:
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
      401:
        description: Unauthorized – Invalid or missing token
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
    if not data:
        raise BadRequestsError("Invalid or missing JSON data")

    # Ensure that the data requirement is present
    required_fields = ['seller_id', 'name', 'description', 'price', 'stock']
    if not all(field in data for field in required_fields):
        raise BadRequestsError("Missing required fields: seller_id, name, description, price, or stock")

    try:
        data['price'] = float(data['price'])
        data['stock'] = int(data['stock'])
    except (ValueError, TypeError):
        raise BadRequestsError("Price must be a number and stock must be an integer")

    if data['price'] < 0 or data['stock'] < 0:
        raise BadRequestsError("Price and stock must be non-negative")

    # Create new product
    new_product = Product(
        seller_id=data['seller_id'],
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )

    # Store new product in database
    db.session.add(new_product)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise

    return jsonify({"message": "Product created", "product": new_product.id}), 201


# Get a product by ID (GET)
@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id: int):
    """
    Get product by ID
    ---
    tags:
      - Products
    summary: Retrieve a product by their unique ID
    description: Endpoint to retrieve a product's data by their unique ID.
    parameters:
      - in: path
        name: id
        required: true
        description: The unique ID of the product to retrieve
        schema:
          type: integer
          example: 123
    responses:
      200:
        description: Product data successfully retrieved
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 123
                seller_id:
                  type: integer
                  example: 123
                name:
                  type: string
                  example: "smartphone"
                description:
                  type: string
                  example: "Xiaomi 13T Plus 250GB octa-core"
                price:
                  type: number
                  format: float
                  example: 125.85
                stock:
                  type: integer
                  example: 35
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
        description: Product not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Product not found"
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
    #product = Product.query.get(id)
    product = db.session.get(Product, id)
    if not product:
        raise ResourceNotFound("Product not found")

    return jsonify({
        "id": product.id,
        "seller_id": product.seller_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "created_at": product.created_at
    }), 200


# Get all products (GET)
@products_bp.route('/products', methods=['GET'])
def get_all_products():
    """
        Get All Products
        ---
        tags:
          - Products
        summary: Retrieve all products
        description: Returns a list of all available products ordered by their ID.
        responses:
          200:
            description: A list of products
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Product ID
                  seller_id:
                    type: integer
                    description: ID of the seller who owns the product
                  name:
                    type: string
                    description: Name of the product
                  description:
                    type: string
                    description: Description of the product
                  price:
                    type: number
                    format: float
                    description: Price of the product
                  stock:
                    type: integer
                    description: Available stock
                  created_at:
                    type: string
                    format: date-time
                    description: Timestamp when the product was created
          404:
            description: No products found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: No products found
        """
    products = Product.query.order_by(Product.id).all()
    if not products:
        raise ResourceNotFound("Products not found")

    # turn the list of objects to a dictionary list
    products_list = [
        {
            "id": product.id,
            "seller_id": product.seller_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "created_at": product.created_at
        }
        for product in products
    ]

    return jsonify(products_list), 200


@products_bp.route('/products/<int:product_id>', methods=['PATCH'])
@token_required
def update_product(product_id: int):
    """
        Update a Product
        ---
        tags:
          - Products
        summary: Update an existing product
        description: Update one or more fields of an existing product by its ID. Requires authentication via token.
        security:
          - Bearer: []
        parameters:
          - name: product_id
            in: path
            type: integer
            required: true
            description: ID of the product to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                seller_id:
                  type: integer
                  description: New seller ID
                name:
                  type: string
                  description: New name of the product
                description:
                  type: string
                  description: New description
                price:
                  type: number
                  format: float
                  description: New price
                stock:
                  type: integer
                  description: New stock quantity
        responses:
          200:
            description: Product updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Product updated successfully
                product:
                  type: object
                  properties:
                    id:
                      type: integer
                    seller_id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    price:
                      type: number
                      format: float
                    stock:
                      type: integer
                    created_at:
                      type: string
                      format: date-time
          404:
            description: Product not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Product not found
        """
    data = request.get_json()
    if not data:
        raise BadRequestsError("Invalid or missing JSON data")

    product = Product.query.get(product_id)

    if not product:
        raise ResourceNotFound("Product not found")

    if 'seller_id' in data:
        product.seller_id = data['seller_id']
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        try:
            data['price'] = float(data['price'])
        except (ValueError, TypeError):
            raise BadRequestsError("Price must be a number")
        if data['price'] < 0:
            raise BadRequestsError("Price must be non-negative")
        product.price = data['price']
    if 'stock' in data:
        try:
            data['stock'] = int(data['stock'])
        except (ValueError, TypeError):
            raise BadRequestsError("Stock must be an integer")
        if data['stock'] < 0:
            raise BadRequestsError("Stock must be non-negative")
        product.stock = data['stock']

    # Safe the changes in database
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise

    # Response
    return jsonify({
        "message": "Product updated  successfully",
        "product": {
            "id": product.id,
            "seller_id": product.seller_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "created_at": product.created_at
        }
    }), 200


@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id: int):
    """
    Delete a user
    ---
    security:
      - BearerAuth: []
    tags:
      - Products
    summary: Delete a user by ID
    description: |
      This endpoint allows an authenticated user to delete a specific user by their `user_id`.

      Requires a valid JWT token in the `Authorization` header.
    parameters:
      - in: header
        name: Authorization
        required: true
        description: JWT token for authentication
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
      - in: path
        name: user_id
        required: true
        description: ID of the user to delete
        schema:
          type: integer
          example: 5

    responses:
      200:
        description: User deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: User deleted successfully
            user_id:
              type: integer
              example: 5
      400:
        description: Invalid user ID
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid user ID
      401:
        description: Unauthorized, invalid or missing token
        schema:
          type: object
          properties:
            error:
              type: string
              example: Token is missing or invalid
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User with id 5 not found
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: Internal server error
    """

    product = Product.query.get(product_id)

    if not product:
        raise ResourceNotFound("Product not found")

    # Delete product
    db.session.delete(product)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise

    # Response
    return jsonify({"message": "Product delete successfully"}), 200
