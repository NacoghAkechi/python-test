"""Use case lập hóa đơn của tháng này (Use Cases).

Chỉ biết thế giới bên ngoài (DB, mail) qua quy ước viết bằng Protocol, không biết gì về Django.
"""

from dataclasses import dataclass
from typing import Protocol

from gas.charge import gas_charge


@dataclass(frozen=True)
class Customer:
    id: int
    email: str
    web_statement: bool  # True: chọn hóa đơn trên web (Web 明細), False: dùng phiếu giấy (検針票)


@dataclass(frozen=True)
class Bill:
    customer_id: int
    usage: int
    amount: int


class CustomerRepository(Protocol):
    def find(self, customer_id: int) -> Customer | None: ...


class BillRepository(Protocol):
    def save(self, bill: Bill) -> int: ...


class Mailer(Protocol):
    def send_bill_mail(self, to: str, amount: int) -> None: ...


class CustomerNotFoundError(Exception):
    pass


def issue_bill(
    customer_id: int,
    usage: int,
    customers: CustomerRepository,
    bills: BillRepository,
    mailer: Mailer,
) -> int:
    """Tính tiền gas từ lượng dùng của tháng này, lưu lại và trả về ID hóa đơn.

    Người chọn Web 明細 thì được gửi mail báo tiền gas.
    """
    customer = customers.find(customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"customer {customer_id} not found")

    amount = gas_charge(usage)
    bill_id = bills.save(Bill(customer_id=customer.id, usage=usage, amount=amount))

    if customer.web_statement:
        mailer.send_bill_mail(customer.email, amount)
    return bill_id
