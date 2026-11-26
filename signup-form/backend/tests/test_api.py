"""Bài ③: test cho API đăng ký (POST /api/signup/).

File này dùng Django REST framework, nên khi bắt đầu bài ③ mới đặt vào backend/tests/.
"""

import pytest
from rest_framework.test import APIClient

from accounts.models import User
from tests.expected_messages import (
    EMAIL_INVALID,
    EMAIL_TAKEN,
    PASSWORD_NO_DIGIT,
    PREF_REQUIRED,
    USERNAME_LENGTH,
    USERNAME_REQUIRED,
)

pytestmark = pytest.mark.django_db

API_URL = "/api/signup/"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def test_valid_request_creates_user(
    api_client: APIClient, valid_data: dict[str, object]
) -> None:
    # Act
    response = api_client.post(API_URL, valid_data, format="json")

    # Assert
    assert response.status_code == 200
    assert response.json()["username"] == "taro"
    assert User.objects.filter(username="taro").exists()


def test_password_is_not_returned(
    api_client: APIClient, valid_data: dict[str, object]
) -> None:
    # Act
    response = api_client.post(API_URL, valid_data, format="json")

    # Assert
    assert "password" not in response.json()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("username", "", USERNAME_REQUIRED),
        ("username", "ab", USERNAME_LENGTH),
        ("email", "taro", EMAIL_INVALID),
        ("password", "password", PASSWORD_NO_DIGIT),
        ("pref", 48, PREF_REQUIRED),
    ],
    ids=["username-empty", "username-ab", "email-taro", "password-password", "pref-48"],
)
def test_invalid_value_returns_400(
    api_client: APIClient,
    valid_data: dict[str, object],
    field: str,
    value: object,
    message: str,
) -> None:
    # Arrange
    data = {**valid_data, field: value}

    # Act
    response = api_client.post(API_URL, data, format="json")

    # Assert
    assert response.status_code == 400
    assert message in response.json()[field]
    assert not User.objects.exists()


def test_duplicate_email_returns_400(
    api_client: APIClient, valid_data: dict[str, object], existing_user: User
) -> None:
    # Arrange
    data = {**valid_data, "email": "hanako@example.com"}

    # Act
    response = api_client.post(API_URL, data, format="json")

    # Assert
    assert response.status_code == 400
    assert EMAIL_TAKEN in response.json()["email"]
