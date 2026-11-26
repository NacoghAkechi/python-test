"""テストで共通に使う fixture。"""

import pytest
from django.core.management import call_command

from accounts.models import Pref


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """テスト用の DB を作ったあと、47 都道府県（accounts/fixtures/prefs.json）を 1 回だけ登録する。

    pytest-django の django_db_setup を上書きしている。
    各テストの変更はロールバックされるが、ここで登録したデータはすべてのテストで残る。
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "prefs")


@pytest.fixture
def tokyo(db):
    """東京都（コード 13）。"""
    return Pref.objects.get(code=13)


@pytest.fixture
def valid_data(tokyo):
    """すべてのルールを通る入力。テストでは、1 つの項目だけを変えて使う。"""
    return {
        "username": "taro",
        "email": "taro@example.com",
        "password": "Passw0rd",
        "tel": "0312345678",
        "pref": tokyo.code,
    }


# TODO: 登録済みのユーザーを作って返す fixture `existing_user` を書く
#       （username は「hanako」、email は「hanako@example.com」）。重複のテストで使う
