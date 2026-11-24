"""API から本物の DB まで通す結合テスト。演習 6 で書き足していく。"""

import pytest
from django.test import Client

from gas.web.models import BillRecord, CustomerRecord

# mailoutbox：メールを送らずに控える。環境によって 5 秒かかるホスト名の問い合わせも省ける
pytestmark = [
    pytest.mark.integration,
    pytest.mark.django_db,
    pytest.mark.usefixtures("mailoutbox"),
]


def test_bill_is_saved_with_charge_for_usage(client: Client) -> None:
    # Arrange
    customer = CustomerRecord.objects.create(
        email="web@example.com", web_statement=True
    )

    # Act
    response = client.post(
        "/api/bills/",
        {"customer_id": customer.id, "usage": 30},
        content_type="application/json",
    )

    # Assert
    assert response.status_code == 201
    bill = BillRecord.objects.get(id=response.json()["bill_id"])
    assert bill.amount == 6488
