import json
from app.models import Product, Order, OrderItem
from app.database import db


def test_create_order_success(client, auth_token):
    product = Product(name="Product A", seller_id=1, price=10.00, stock=100,
                      description="Xiaomi 13T Plus 250GB octa-core")
    db.session.add(product)
    db.session.commit()

    data = {
        "buyer_id": 1,
        "products": [{"product_id": product.id, "quantity": 2}]
    }

    response = client.post(
        "/orders",
        json=data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["message"] == "Order created"
    assert body["total"] == 20.0


def test_create_order_missing_fields(client, auth_token):
    data = {
        "products": [{"product_id": 1, "quantity": 2}]
    }

    response = client.post(
        "/orders",
        json=data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 400
    assert "buyer_id" in response.get_json()["message"]


def test_create_order_product_not_found(client, auth_token):
    data = {
        "buyer_id": 1,
        "products": [{"product_id": 999, "quantity": 2}]
    }

    response = client.post(
        "/orders",
        json=data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 404
    assert "Product with id 999 not found" in response.get_json()["message"]


def test_get_order_success(client, auth_token):
    product = Product(name="Product A", seller_id=1, price=10.00, stock=100,
                      description="Xiaomi 13T Plus 250GB octa-core")
    db.session.add(product)

    order = Order(buyer_id=1, total=10.00, status="pending")
    db.session.add(order)
    db.session.flush()

    item = OrderItem(order_id=order.id, product_id=product.id, quantity=2, price=5.00)
    db.session.add(item)
    db.session.commit()

    response = client.get(
        f"/orders/{order.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    assert response.get_json()["total"] == 10.0


def test_get_order_not_found(client, auth_token):
    response = client.get(
        "/orders/999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 404
    assert "Order not found" in response.get_json()["message"]


def test_create_order_no_token(client):
    data = {
        "buyer_id": 1,
        "products": [{"product_id": 1, "quantity": 2}]
    }

    response = client.post("/orders", json=data)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Token Missing"
    assert data["message"] == "Authorization token is missing"
