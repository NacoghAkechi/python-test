"""本物の HTTP サーバーを立てて、外から請求を作るテスト。"""

import json
from typing import Any
from urllib.request import ProxyHandler, Request, build_opener

import pytest
from pytest_django.live_server_helper import LiveServer

from gas.web.models import BillRecord, CustomerRecord

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.django_db(transaction=True),
    pytest.mark.usefixtures("mailoutbox"),
]


def post_json(url: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    request = Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    # 社内プロキシを通さず、手元のサーバーに直接つなぐ
    opener = build_opener(ProxyHandler({}))
    with opener.open(request) as response:
        return response.status, json.load(response)


def test_bill_can_be_issued_over_http(live_server: LiveServer) -> None:
    # Arrange
    customer = CustomerRecord.objects.create(
        email="web@example.com", web_statement=True
    )

    # Act
    status, body = post_json(
        f"{live_server.url}/api/bills/", {"customer_id": customer.id, "usage": 30}
    )

    # Assert
    assert status == 201
    assert BillRecord.objects.get(id=body["bill_id"]).amount == 6488
