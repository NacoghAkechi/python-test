"""課題①: 登録画面（/signup/）と完了画面（/signup/done/）のテスト。"""

import pytest
from pytest_django.asserts import assertContains, assertRedirects

from accounts.models import User
from tests.expected_messages import USERNAME_TOO_SHORT

pytestmark = pytest.mark.django_db

SIGNUP_URL = "/signup/"
DONE_URL = "/signup/done/"


def test_signup_page_shows_form(client):
    response = client.get(SIGNUP_URL)

    assert response.status_code == 200
    for name in ["username", "email", "password", "tel", "pref"]:
        assertContains(response, f'name="{name}"')
    assertContains(response, "東京都")


def test_valid_post_redirects_to_done_page(client, valid_data):
    response = client.post(SIGNUP_URL, valid_data)

    assertRedirects(response, SIGNUP_URL)
    assert User.objects.filter(username="taro").exists()


def test_invalid_post_shows_errors_and_saves_nothing(client, valid_data):
    response = client.post(SIGNUP_URL, {**valid_data, "username": "ab"})

    assert response.status_code == 200
    assertContains(response, USERNAME_TOO_SHORT)
    assert not User.objects.exists()
