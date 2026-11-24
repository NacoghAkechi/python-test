"""Đáp ứng quy ước Protocol bằng ORM của Django (Interface Adapters)."""

from gas.billing import Bill, Customer
from gas.web.models import BillRecord, CustomerRecord


class DjangoCustomerRepository:
    def find(self, customer_id: int) -> Customer | None:
        record = CustomerRecord.objects.filter(id=customer_id).first()
        if record is None:
            return None
        return Customer(
            id=record.id,
            email=record.email,
            web_statement=record.web_statement,
        )


class DjangoBillRepository:
    def save(self, bill: Bill) -> int:
        record = BillRecord.objects.create(
            customer_id=bill.customer_id, usage=bill.usage, amount=bill.amount
        )
        return record.id
