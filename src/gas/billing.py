"""今月の請求を作るユースケース（Use Cases）。

外の世界（DB・メール）は Protocol で書いた約束だけを知っていて、Django は知らない。
"""

from dataclasses import dataclass
from typing import Protocol

from gas.charge import gas_charge


@dataclass(frozen=True)
class Customer:
    id: int
    email: str
    web_statement: bool  # Web 明細を選んだ人は True、紙の検針票の人は False


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
    """今月の使用量からガス料金を計算して保存し、請求 ID を返す。

    Web 明細の人には、料金のお知らせメールを送る。
    """
    customer = customers.find(customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"customer {customer_id} not found")

    amount = gas_charge(usage)
    bill_id = bills.save(Bill(customer_id=customer.id, usage=usage, amount=amount))

    if customer.web_statement:
        mailer.send_bill_mail(customer.email, amount)
    return bill_id
