"""課題①: 登録フォーム（accounts.forms.SignupForm）のテスト。"""

import pytest

from accounts.forms import SignupForm
from accounts.models import User
from tests.expected_messages import (
    EMAIL_INVALID,
    EMAIL_REQUIRED,
    PASSWORD_NO_LOWER,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    USERNAME_INVALID,
    USERNAME_REQUIRED,
    USERNAME_TAKEN,
    USERNAME_TOO_SHORT,
)

pytestmark = pytest.mark.django_db


def test_valid_data_passes(valid_data: dict[str, object]) -> None:
    # Arrange
    form = SignupForm(data=valid_data)

    # Act
    is_valid = form.is_valid()

    # Assert
    assert is_valid, form.errors


def test_save_stores_user(valid_data: dict[str, object]) -> None:
    # Arrange
    form = SignupForm(data=valid_data)

    # Act
    form.save()

    # Assert
    user = User.objects.get(username="taro")
    assert user.email == "taro@example.com"
    assert user.password


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("username", "", USERNAME_REQUIRED),
        ("username", "abc", USERNAME_TOO_SHORT),
        ("username", "taro yamada", USERNAME_INVALID),
        ("email", "", EMAIL_REQUIRED),
        ("email", "taro", EMAIL_INVALID),
        ("password", "", PASSWORD_REQUIRED),
        ("password", "Pass0rd", PASSWORD_TOO_SHORT),
        ("password", "passw0rd", PASSWORD_NO_LOWER),
    ],
    ids=[
        "username-empty",
        "username-abc",
        "username-with-space",
        "email-empty",
        "email-taro",
        "password-empty",
        "password-Pass0rd",
        "password-passw0rd",
    ],
)
def test_invalid_value_is_rejected(
    valid_data: dict[str, object], field: str, value: str, message: str
) -> None:
    # Arrange
    form = SignupForm(data={**valid_data, field: value})

    # Act
    is_valid = form.is_valid()

    # Assert
    assert not is_valid
    assert message in form.errors[field]


def test_duplicate_username_is_rejected(
    valid_data: dict[str, object], existing_user: User
) -> None:
    # Arrange
    form = SignupForm(data={**valid_data, "username": "hanako"})

    # Act
    is_valid = form.is_valid()

    # Assert
    assert not is_valid
    assert USERNAME_TAKEN in form.errors["username"]
