import pytest
from unittest.mock import patch
from app.models import Product


@pytest.fixture
def new_product_payload():
    return {
        "seller_id": 1,
        "name": "Smartphone",
        "description": "Xiaomi 13T Plus 250GB octa-core",
        "price": 125.85,
        "stock": 35
    }


def test_create_product_success(client, auth_token, new_product_payload):
    headers = {"Authorization": f"Bearer {auth_token}"}

    with patch("app.routes.products.db.session.add") as mock_add, \
         patch("app.routes.products.db.session.commit"):
        response = client.post("/products", json=new_product_payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Product created"
    assert "product" in data


def test_create_product_missing_fields(client, auth_token):
    payload = {
        "seller_id": 1,
        "name": "Product Incomplete"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/products", json=payload, headers=headers)

    assert response.status_code == 400
    data = response.get_json()
    assert data["message"].startswith("Missing required fields")


def test_create_product_invalid_price_and_stock(client, auth_token, new_product_payload):
    headers = {"Authorization": f"Bearer {auth_token}"}
    new_product_payload["price"] = "not_a_number"
    new_product_payload["stock"] = "abc"

    response = client.post("/products", json=new_product_payload, headers=headers)

    assert response.status_code == 400
    data = response.get_json()
    assert "Price must be a number" in data["message"]


def test_create_product_negative_price(client, auth_token, new_product_payload):
    headers = {"Authorization": f"Bearer {auth_token}"}
    new_product_payload["price"] = -50
    response = client.post("/products", json=new_product_payload, headers=headers)

    assert response.status_code == 400
    data = response.get_json()
    assert "non-negative" in data["message"]


def test_create_product_no_token(client, new_product_payload):
    response = client.post("/products", json=new_product_payload)
    assert response.status_code == 401
    data = response.get_json()
    assert "token" in data["error"].lower()


def test_create_product_db_error(client, auth_token, new_product_payload):
    headers = {"Authorization": f"Bearer {auth_token}"}

    with patch("app.routes.products.db.session.commit", side_effect=Exception("DB Error")), \
         patch("app.routes.products.db.session.rollback"):
        response = client.post("/products", json=new_product_payload, headers=headers)

    assert response.status_code == 500


@patch("app.routes.products.db.session.get")
def test_get_product_success(mock_get, client):
    product_id = 1
    mock_get.return_value = Product(
        id=1, seller_id=1, name="Smartphone", description="Good phone", price=120.5, stock=10
    )
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200


def test_get_product_not_found(client):
    with patch("app.routes.products.Product.query.get", return_value=None):
        response = client.get("/products/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Resource Not Found"
    assert data["message"] == "Product not found"

