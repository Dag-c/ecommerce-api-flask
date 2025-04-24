import pytest
from unittest.mock import patch
from app.models import User

@pytest.fixture
def new_user_payload():
    return {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "mypassword123",
        "role": "buyer"
    }

def test_create_user_success(client, new_user_payload):
    with patch("app.routes.users.User.query") as mock_query, \
         patch("app.routes.users.encrypt_password", return_value="hashed_password"):
        mock_query.filter_by.return_value.first.return_value = None

        response = client.post("/users", json=new_user_payload)

        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "User created"
        assert "user" in data

def test_create_user_missing_fields(client):
    payload = {
        "email": "bob@example.com",
        "password": "pass123"
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"
    assert data["message"] == "Missing required fields: name, email, or password"

def test_create_user_email_already_registered(client, new_user_payload):
    with patch("app.routes.users.User.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = User(
            id=1, name="Existing User", email=new_user_payload["email"], password="hashed"
        )
        response = client.post("/users", json=new_user_payload)

        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Bad Request"
        assert data["message"] == "Email already registered"

def test_create_user_unexpected_error(client, new_user_payload):
    with patch("app.routes.users.User.query") as mock_query, \
         patch("app.routes.users.encrypt_password", return_value="hashed_pass"), \
         patch("app.routes.users.db.session.add", side_effect=Exception("DB Error")):
        mock_query.filter_by.return_value.first.return_value = None

        response = client.post("/users", json=new_user_payload)

        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Internal Server Error"
        assert data["message"] == "An unexpected error occurred"


def test_get_users(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/users", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_users_no_token(client):
    response = client.get("/users")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Token Missing"
    assert data["message"] == "Authorization token is missing"


def test_get_users_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.value"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid Token"
    assert data["message"] == "The token is invalid"


def test_update_user(client, auth_token):
    update_data = {
        "name": "Juan Pérez Actualizado",
        "email": "juan.perez.actualizado@example.com",
        "password": "newpassword456",
        "role": "seller"
    }

    user_id = 1  # Suponiendo que el usuario con ID 1 existe

    headers = {"Authorization": f"Bearer {auth_token}"}

    # Realizar la solicitud PATCH para actualizar el usuario
    response = client.patch(f"/users/{user_id}", json=update_data, headers=headers)

    # Verificar que la actualización fue exitosa
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User updated successfully"
    assert data["user"]["name"] == update_data["name"]
    assert data["user"]["email"] == update_data["email"]
    assert data["user"]["role"] == update_data["role"]


def test_update_user_not_found(client, auth_token):
    update_data = {
        "name": "Juan Pérez Actualizado",
        "email": "juan.perez.actualizado@example.com",
        "password": "newpassword456",
        "role": "seller"
    }

    user_id = 999

    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.patch(f"/users/{user_id}", json=update_data, headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Resource Not Found"
    assert data["message"] == "User not found"


def test_update_user_invalid_token(client):
    update_data = {
        "name": "Juan Pérez Actualizado",
        "email": "juan.perez.actualizado@example.com",
        "password": "newpassword456",
        "role": "seller"
    }

    user_id = 1

    headers = {"Authorization": "Bearer invalid_token"}

    response = client.patch(f"/users/{user_id}", json=update_data, headers=headers)

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid Token"
    assert data["message"] == "The token is invalid"


def test_delete_user(client, auth_token):
    user_id = 1

    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.delete(f"/users/{user_id}", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User delete successfully"


def test_delete_user_not_found(client, auth_token):
    user_id = 999

    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.delete(f"/users/{user_id}", headers=headers)

    # Verificar que la respuesta sea un error 404
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Resource Not Found"
    assert data["message"] == "User not found"


def test_delete_user_invalid_token(client):
    user_id = 1

    headers = {"Authorization": "Bearer invalid_token"}

    response = client.delete(f"/users/{user_id}", headers=headers)

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid Token"
    assert data["message"] == "The token is invalid"

