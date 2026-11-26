"""課題③: 登録 API（POST /api/signup/）のテスト。

Django REST framework を使うので、課題③を始めたら backend/tests/ に入れる。
"""

import pytest
from rest_framework.test import APIClient

from accounts.models import User
from tests.expected_messages import (
    EMAIL_INVALID,
    EMAIL_TAKEN,
    PASSWORD_NO_UPPER,
    PREF_NOT_FOUND,
    USERNAME_REQUIRED,
    USERNAME_TOO_SHORT,
)

pytestmark = pytest.mark.django_db

API_URL = "/api/signup/"


@pytest.fixture
def api_client():
    return APIClient()


def test_valid_request_creates_user(api_client, valid_data):
    response = api_client.post(API_URL, valid_data, format="json")

    assert response.status_code == 200
    assert response.json()["username"] == "taro"
    assert User.objects.filter(username="taro").exists()


def test_password_is_not_returned(api_client, valid_data):
    response = api_client.post(API_URL, valid_data, format="json")

    assert "password" not in response.json()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("username", "", USERNAME_REQUIRED),
        ("username", "ab", USERNAME_TOO_SHORT),
        ("email", "taro", EMAIL_INVALID),
        ("password", "passw0rd", PASSWORD_NO_UPPER),
        ("pref", 48, PREF_NOT_FOUND),
    ],
)
def test_invalid_value_returns_400(api_client, valid_data, field, value, message):
    response = api_client.post(API_URL, {**valid_data, field: value}, format="json")

    assert response.status_code == 400
    assert message in response.json()[field]
    assert not User.objects.exists()


def test_duplicate_email_returns_400(api_client, valid_data, existing_user):
    data = {**valid_data, "email": "hanako@example.com"}

    response = api_client.post(API_URL, data, format="json")

    assert response.status_code == 400
    assert EMAIL_TAKEN in response.json()["email"]
