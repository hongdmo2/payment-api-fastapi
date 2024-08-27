import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from app.auth import create_access_token, get_password_hash
from app.models import User


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com",
              "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login(client: TestClient, db_session: Session):
    hashed_password = get_password_hash("testpassword")
    user = User(username="testuser", email="test@example.com",
                hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_route(client: TestClient, db_session: Session):
    # Create a user
    user = User(username="testuser", email="test@example.com",
                hashed_password="hashedpass")
    db_session.add(user)
    db_session.commit()

    # Create a token
    access_token = create_access_token(data={"sub": user.username})

    # Test accessing a protected route
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_protected_route_without_token(client: TestClient):
    response = client.get("/users/me/")
    assert response.status_code == 401
