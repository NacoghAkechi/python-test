"""Integration test chạy xuyên suốt từ API đến DB thật. Viết thêm ở bài 6."""

import pytest
from django.test import Client

from gas.web.models import BillRecord, CustomerRecord

# mailoutbox: giữ lại mail mà không gửi thật. Cũng tránh được bước tra tên máy có thể mất 5 giây tùy môi trường
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
