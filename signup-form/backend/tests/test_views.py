"""課題①: 登録画面（/signup/）と完了画面（/signup/done/）のテスト。"""

import pytest
from django.test import Client
from pytest_django.asserts import assertContains, assertRedirects

from accounts.models import User
from tests.expected_messages import USERNAME_LENGTH

pytestmark = pytest.mark.django_db

SIGNUP_URL = "/signup/"
DONE_URL = "/signup/done/"


def test_signup_page_shows_form(client: Client) -> None:
    # Act
    response = client.get(SIGNUP_URL)

    # Assert
    assert response.status_code == 200
    for name in ["username", "email", "password", "pref"]:
        assertContains(response, f'name="{name}"')
    assertContains(response, "東京都")


def test_valid_post_redirects_to_done_page(
    client: Client, valid_data: dict[str, object]
) -> None:
    # Act
    response = client.post(SIGNUP_URL, valid_data)

    # Assert
    assertRedirects(response, SIGNUP_URL)
    assert User.objects.filter(username="taro").exists()


def test_invalid_post_shows_errors_and_saves_nothing(
    client: Client, valid_data: dict[str, object]
) -> None:
    # Arrange
    data = {**valid_data, "username": "ab"}

    # Act
    response = client.post(SIGNUP_URL, data)

    # Assert
    assert response.status_code == 200
    assertContains(response, USERNAME_LENGTH)
    assert not User.objects.exists()
