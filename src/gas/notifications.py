"""ガスが止まったことを知らせるユースケース（Use Cases）。

メーターの状態は外部のメーター監視システムに聞き、メールは外部のメールサービスに頼む。
どちらも Protocol で書いた約束だけを知っている。
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
    """メーターがガスを止めていれば、登録した全員にお知らせを送り、送った人数を返す。"""
    if not meter.is_shut_off(meter_id):
        return 0
    for email in emails:
        mailer.send_shutoff_mail(email, meter_id)
    return len(emails)
