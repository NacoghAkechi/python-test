"""Protocol の約束を、Django のメール送信で満たす（Interface Adapters）。"""

from django.core.mail import send_mail

from gas.labels import format_price


class DjangoMailer:
    def send_bill_mail(self, to: str, amount: int) -> None:
        send_mail(
            subject="今月のガス料金のお知らせ",
            message=f"今月のガス料金は {format_price(amount)} です",
            from_email="gas@example.com",
            recipient_list=[to],
        )
