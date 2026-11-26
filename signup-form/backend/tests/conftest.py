"""Các fixture dùng chung cho các test."""

import pytest
from django.core.management import call_command

from accounts.models import Pref


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker) -> None:
    """Sau khi tạo DB cho test, nạp 47 tỉnh thành (accounts/fixtures/prefs.json) đúng 1 lần.

    Fixture này ghi đè django_db_setup của pytest-django.
    Thay đổi trong từng test sẽ bị rollback, nhưng dữ liệu nạp ở đây còn nguyên cho mọi test.
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "prefs")


@pytest.fixture
def tokyo(db) -> Pref:
    """Tokyo (東京都, mã 13)."""
    return Pref.objects.get(code=13)


@pytest.fixture
def valid_data(tokyo: Pref) -> dict[str, object]:
    """Dữ liệu nhập hợp lệ với mọi quy tắc. Trong test, chỉ đổi 1 trường rồi dùng."""
    return {
        "username": "taro",
        "email": "taro@example.com",
        "password": "Passw0rd",
        "tel": "0312345678",
        "pref": tokyo.code,
    }


# TODO: viết fixture `existing_user` tạo và trả về một người dùng đã đăng ký
#       (username là "hanako", email là "hanako@example.com"). Dùng cho các test trùng lặp
