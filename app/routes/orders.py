from flask import Blueprint, request, jsonify
from app.models import Order, Product, OrderItem
from app.database import db
from app.services.auth import token_required
from app.utils.exceptions import ResourceNotFound, BadRequestsError

# Create a Blueprint for orders
orders_bp = Blueprint('orders', __name__)


# Create a new order
@orders_bp.route('/orders', methods=['POST'])
@token_required
def create_order():
    """
            Create a new order.
            ---
            security:
              - BearerAuth: []
            tags:
              - Orders
            summary: Create a new order with a list of products
            description: |
              This endpoint allows an authenticated user to create a new order by providing a `buyer_id` and a list of products.
              Each product in the list must include a `product_id` and a `quantity`. The total price will be automatically calculated.

              Requires a valid JWT token in the `Authorization` header.

            parameters:
              - in: header
                name: Authorization
                required: true
                description: JWT token for authentication
                schema:
                  type: string
                  example: "Bearer your_jwt_token_here"
              - in: body
                name: order
                required: true
                description: JSON object containing buyer ID and products
                schema:
                  type: object
                  required:
                    - buyer_id
                    - products
                  properties:
                    buyer_id:
                      type: integer
                      example: 2
                    products:
                      type: array
                      items:
                        type: object
                        required:
                          - product_id
                          - quantity
                        properties:
                          product_id:
                            type: integer
                            example: 1
                          quantity:
                            type: integer
                            example: 2

            responses:
              201:
                description: Order created successfully
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: Order created
                    order_id:
                      type: integer
                      example: 123
                    buyer_id:
                      type: integer
                      example: 2
                    total:
                      type: number
                      format: float
                      example: 19.99
                    status:
                      type: string
                      example: pending
                    created_at:
                      type: string
                      example: "2025-04-04T14:55:22"
                    order_products:
                      type: array
                      items:
                        type: object
                        properties:
                          product_id:
                            type: integer
                            example: 1
                          quantity:
                            type: integer
                            example: 2
                          price:
                            type: number
                            format: float
                            example: 9.99

              400:
                description: Invalid input or missing data
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Bad request"
                    message:
                      type: string
                      example: "buyer_id and products list are required"

              401:
                description: Unauthorized, invalid or expired token
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Invalid token"
                    message:
                      type: string
                      example: "Signature verification failed"

              403:
                description: Forbidden – token missing
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Token missing"
                    message:
                      type: string
                      example: "Authorization header is required"

              404:
                description: Product not found
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Resource not found"
                    message:
                      type: string
                      example: "Product with id 99 not found"

              429:
                description: Too many requests – rate limit exceeded
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
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Internal Server Error"
                    message:
                      type: string
                      example: "An unexpected error occurred"

    """

    data = request.get_json()

    if not data:
        raise BadRequestsError("Invalid or missing JSON data")

    # Ensure that the data requirement is present
    required_fields = ['buyer_id', 'products']
    if not all(field in data for field in required_fields):
        raise BadRequestsError("Missing required fields: buyer_id or products")

    try:
        # Create new order
        new_order = Order(
            buyer_id=data['buyer_id'],
            total=0.01,
            status="pending"
        )

        db.session.add(new_order)
        db.session.flush()  # assign an id before to make a commit

        total_price = 0
        order_products = []
        order_re_products = [p for p in data['products']]
        products_db = {p.id: p for p in Product.query.filter(Product.id.in_(product.get('product_id') for product in
                                                                            order_re_products)).all()}

        for product in order_re_products:

            if not product.get('product_id') or not product.get('quantity'):
                raise BadRequestsError("Each product must have 'product_id' and 'quantity'")
            try:
                product["product_id"] = int(product["product_id"])
                product["quantity"] = int(product["quantity"])
            except (ValueError, TypeError):
                raise BadRequestsError("product_id must be an integer and quantity must be an integer")

            if product["product_id"] < 0 or product["quantity"] <= 0:
                raise BadRequestsError("Product_id must be non-negative and quantity must be greater than 0")

            product_db = products_db.get(product["product_id"])
            if not product_db:
                raise ResourceNotFound(f"Product with id {product["product_id"]} not found")
            total_price += product_db.price * product["quantity"]
            order_item = OrderItem(
                order=new_order,
                product_id=product["product_id"],
                quantity=product["quantity"],
                price=product_db.price
            )
            order_products.append(order_item)
        db.session.add_all(order_products)

        new_order.total = total_price
        db.session.commit()

        return jsonify({
            "message": "Order created",
            "order_id": new_order.id,
            "buyer_id": new_order.buyer_id,
            "total": round(float(new_order.total), 2),
            "status": new_order.status,
            "created_at": new_order.created_at,
            "order_products": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": round(float(item.price), 3),
                } for item in new_order.order_products
            ]
        }), 201
    except Exception as e:
        db.session.rollback()
        raise


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id: int) -> tuple:
    """
    Get details of a specific order by ID.
    ---
    security:
      - BearerAuth: []
    tags:
      - Orders
    summary: Retrieve details of an order by its ID
    description: |
      This endpoint allows an authenticated user to retrieve the details of a specific order by its `order_id`.

      It returns all relevant information about the order, including:
        - Buyer's ID
        - Order total
        - Order status
        - Date and time of creation
        - List of associated products (with quantity and price)

      A valid JWT token must be included in the `Authorization` header.

    parameters:
      - in: header
        name: Authorization
        required: true
        description: JWT token for authentication
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
      - in: path
        name: order_id
        required: true
        description: ID of the order to retrieve
        schema:
          type: integer
          example: 1

    responses:
      200:
        description: Order details retrieved successfully
        schema:
          type: object
          properties:
            order_id:
              type: integer
              example: 123
            buyer_id:
              type: integer
              example: 2
            total:
              type: number
              format: float
              example: 19.99
            status:
              type: string
              example: pending
            created_at:
              type: string
              example: "2025-04-04T14:55:22"
            order_products:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    example: 1
                  quantity:
                    type: integer
                    example: 2
                  price:
                    type: number
                    format: float
                    example: 9.99
      400:
        description: Bad request or invalid token format
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
            message:
              type: string
              example: "Some explanation here"
      401:
        description: Unauthorized - token invalid or expired
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Token is missing or invalid"
            message:
              type: string
              example: "Token expired"
      403:
        description: Forbidden - token missing
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Token missing"
            message:
              type: string
              example: "Authorization header not provided"
      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order not found"
            message:
              type: string
              example: "No order matches the given ID"
      429:
        description: Too many requests - rate limit exceeded
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
        description: Internal server or database error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal Server Error"
            message:
              type: string
              example: "An unexpected error occurred"
    """

    #order = Order.query.get(order_id)
    order = db.session.get(Order, order_id)

    if not order:
        raise ResourceNotFound("Order not found")

    return jsonify({
        "order_id": order.id,
        "buyer_id": order.buyer_id,
        "total": round(float(order.total), 2),
        "status": order.status,
        "created_at": order.created_at,
        "order_products": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": round(float(item.price), 3),
            } for item in order.order_products
        ]
    }), 200


@orders_bp.route('/orders', methods=['GET'])
@token_required
def get_all_orders() -> tuple:
    """
    Get a list of all orders.
    ---
    tags:
      - Orders
    summary: Retrieve a list of all orders
    description: >
      This endpoint allows an authenticated user to retrieve all orders in the system.
      It requires a valid JWT token sent in the Authorization header as a Bearer token.
      Each order includes buyer ID, total, status, creation date, and the products in the order.

    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: "Bearer token for authentication. Example: Bearer your_token_here"

    security:
      - BearerAuth: []

    responses:
      200:
        description: List of all orders retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: integer
                example: 123
              buyer_id:
                type: integer
                example: 2
              total:
                type: number
                format: float
                example: 19.99
              status:
                type: string
                example: pending
              created_at:
                type: string
                example: "2025-04-04T14:55:22"
              order_products:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                      example: 1
                    quantity:
                      type: integer
                      example: 2
                    price:
                      type: number
                      format: float
                      example: 9.99
      400:
        description: Bad request or invalid token format
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
            message:
              type: string
              example: "Missing required parameters"
      401:
        description: Unauthorized - Invalid or expired token
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Token expired"
            message:
              type: string
              example: "The token has expired"
      403:
        description: Forbidden - Token missing
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Token missing"
            message:
              type: string
              example: "Authorization token is required"
      404:
        description: Resource not found (No orders found)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Resource not found"
            message:
              type: string
              example: "Not orders found"
      429:
        description: Too many requests
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
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal Server Error"
            message:
              type: string
              example: "An unexpected error occurred"
    """
    orders = Order.query.all()

    if not orders:
        raise ResourceNotFound("No orders found")

    orders_list = [
        {
            "order_id": order.id,
            "buyer_id": order.buyer_id,
            "total": round(float(order.total), 2),
            "status": order.status,
            "created_at": order.created_at,
            "order_products": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": round(float(item.price), 3),
                } for item in order.order_products
            ]
        }
        for order in orders
    ]

    return jsonify(orders_list), 200


@orders_bp.route('/orders/buyer/<int:buyer_id>', methods=['GET'])
@token_required
def get_orders_buyer(buyer_id: int) -> tuple:
    """
    Get all orders for a specific buyer by buyer ID.
    ---
    security:
      - BearerAuth: []
    tags:
      - Orders
    summary: Retrieve all orders for a specific buyer
    description: |
      This endpoint allows an authenticated user to retrieve all orders made by a specific buyer identified by their `buyer_id`.

      Requires a valid JWT token in the `Authorization` header (e.g., "Bearer your_token_here").

    parameters:
      - in: path
        name: buyer_id
        required: true
        description: ID of the buyer whose orders are to be retrieved
        type: integer
      - name: Authorization
        in: header
        required: true
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
        description: "Bearer token for authentication. Example: Bearer your_token_here"

    responses:
      200:
        description: List of orders for the buyer retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: integer
                example: 123
              buyer_id:
                type: integer
                example: 2
              total:
                type: number
                format: float
                example: 19.99
              status:
                type: string
                example: pending
              created_at:
                type: string
                example: "2025-04-04T14:55:22"
              order_products:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                      example: 1
                    quantity:
                      type: integer
                      example: 2
                    price:
                      type: number
                      format: float
                      example: 9.99
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad Request"
            message:
              type: string
              example: "Missing required parameter"
      401:
        description: Unauthorized, invalid or missing token
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unauthorized"
            message:
              type: string
              example: "Token is missing or invalid"
      404:
        description: No orders found for this buyer
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Resource not found"
            message:
              type: string
              example: "No orders found for this buyer"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal Server Error"
            message:
              type: string
              example: "An unexpected error occurred"
    """
    orders = Order.query.filter_by(buyer_id=buyer_id).all()

    if not orders:
        raise ResourceNotFound("No orders found for this buyer")

    orders_list = [
        {
            "order_id": order.id,
            "buyer_id": order.buyer_id,
            "total": round(float(order.total), 2),
            "status": order.status,
            "created_at": order.created_at,
            "order_products": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": round(float(item.price), 2),
                } for item in order.order_products
            ]
        }
        for order in orders
    ]

    return jsonify(orders_list), 200


@orders_bp.route('/orders/<int:order_id>', methods=['PATCH'])
@token_required
def update_order(order_id):
    """
    Update the status of an existing order by ID.
    ---
    security:
      - BearerAuth: []
    tags:
      - Orders
    summary: Update order status by order ID
    description: |
      This endpoint allows an authenticated user to update the **status** of an existing order.

      Only the **`status`** field is allowed to be updated. Fields such as **`total`**, **`order_products`**, or others cannot be modified.

      Orders that are already marked as **`shipped`** or **`delivered`** cannot be updated.

      If the new status is **`shipped`**, the system will verify that sufficient stock exists for each product in the order.
      If any product lacks available stock, the update will be rejected.

      **Allowed values for the `status` field:**
        - `pending`
        - `shipped`
        - `delivered`

      Requires a valid JWT token in the `Authorization` header (e.g., "Bearer your_token_here").

    parameters:
      - in: path
        name: order_id
        required: true
        description: ID of the order to be updated
        type: integer
        example: 123

      - name: Authorization
        in: header
        required: true
        schema:
          type: string
          example: "Bearer your_jwt_token_here"
        description: Bearer token for authentication.

      - in: body
        name: body
        required: true
        description: JSON object with the new order status
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [pending, shipped, delivered]
              example: shipped

    responses:
      200:
        description: Order status updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Order status updated successfully
            order_id:
              type: integer
              example: 123
            status:
              type: string
              example: shipped

      400:
        description: Invalid update attempt
        schema:
          type: object
          properties:
            error:
              type: string
              example: Bad request
            message:
              type: string
              example: Cannot modify an order that has already been shipped or delivered

      401:
        description: Invalid or expired token
        schema:
          type: object
          properties:
            error:
              type: string
              example: Token expired
            message:
              type: string
              example: Your token has expired. Please log in again.

      403:
        description: Missing token
        schema:
          type: object
          properties:
            error:
              type: string
              example: Token missing
            message:
              type: string
              example: You must include a token in the Authorization header.

      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Resource not found
            message:
              type: string
              example: Order not found

      429:
        description: Too many requests
        schema:
          type: object
          properties:
            error:
              type: string
              example: Too many requests
            message:
              type: string
              example: You have exceeded the allowed rate limit. Try again later.

      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: Internal Server Error
            message:
              type: string
              example: An unexpected error occurred
    """
    data = request.get_json()
    if not data:
        raise BadRequestsError("Invalid or missing JSON data")

    order = Order.query.get(order_id)

    if not order:
        raise ResourceNotFound("Order not found")

    if order.status in ['shipped', 'delivered']:
        raise BadRequestsError("Cannot modify an order that has already been shipped or delivered")

    allowed_fields = ['status']

    for key, value in data.items():
        if key in allowed_fields:
            if key == 'status' and value == 'shipped':
                for product in order.order_products:
                    product_db = Product.query.get(product.product_id)
                    if product_db.stock < product.quantity:
                        db.session.rollback()
                        raise BadRequestsError(f"There is not enough stock of {product_db.name} to complete the order")

                for product in order.order_products:
                    product_db = Product.query.get(product.product_id)
                    product_db.stock -= product.quantity

            setattr(order, key, value)

    try:
        db.session.commit()
        return jsonify({
            'message': 'Order updated successfully',
            "order_id": order.id,
            "buyer_id": order.buyer_id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at
        }), 200
    except Exception as e:
        db.session.rollback()
        raise


@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@token_required
def delete_order(order_id: int) -> tuple:
    """
    Delete an order by ID.
    ---
    security:
      - BearerAuth: []
    tags:
      - Orders
    summary: Delete an order by order ID
    description: |
      This endpoint allows an authenticated user to delete an order by its ID.

      If the order is found, it will be deleted from the database.
      If the order is not found, a 404 error is returned.
      If there's a problem during the deletion process, a 500 error will be returned.

      Requires a valid JWT token in the `Authorization` header.

    parameters:
      - in: path
        name: order_id
        required: true
        description: ID of the order to be deleted
        type: integer
        example: 123

      - name: Authorization
        in: header
        required: true
        type: string
        example: "Bearer your_jwt_token_here"
        description: Bearer token for authentication.

    responses:
      200:
        description: Order deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order deleted successfully"

      400:
        description: Invalid request, unable to delete the order
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad Request"
            message:
              type: string
              example: "The request could not be processed due to invalid data"

      401:
        description: Unauthorized, missing or invalid token
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unauthorized"
            message:
              type: string
              example: "Token is missing or invalid"

      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order not found"
            message:
              type: string
              example: "The order with the given ID could not be found"

      500:
        description: Internal server error when deleting the order
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal Server Error"
            message:
              type: string
              example: "Failed to delete the order due to a server issue"
    """
    order = Order.query.get(order_id)

    if not order:
        raise ResourceNotFound("Order not found")

    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        raise
