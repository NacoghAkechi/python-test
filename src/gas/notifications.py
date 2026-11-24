"""Use case báo gas bị ngắt (Use Cases).

Trạng thái đồng hồ thì hỏi hệ thống giám sát bên ngoài, gửi mail thì nhờ dịch vụ mail bên ngoài.
Với cả hai, code ở đây chỉ biết quy ước viết bằng Protocol.
"""

from typing import Protocol


class MeterClient(Protocol):
    def is_shut_off(self, meter_id: str) -> bool: ...


class ShutoffMailer(Protocol):
    def send_shutoff_mail(self, to: str, meter_id: str) -> None: ...


def notify_shutoff(
    emails: list[str],
    meter_id: str,
    meter: MeterClient,
    mailer: ShutoffMailer,
) -> int:
    """Nếu đồng hồ đang ngắt gas thì báo cho tất cả người đã đăng ký, rồi trả về số người đã gửi."""
    if not meter.is_shut_off(meter_id):
        return 0
    for email in emails:
        mailer.send_shutoff_mail(email, meter_id)
    return len(emails)
