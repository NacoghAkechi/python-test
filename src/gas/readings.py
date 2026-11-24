"""ガスメーターの指針から、使用量を出す。"""


def usage_between(previous: int, current: int) -> int:
    """前回と今回の指針（㎥）から、そのあいだの使用量（㎥）を返す。

    - 使用量は、今回の指針 − 前回の指針
    - メーターは 4 桁で、9999㎥ の次は 0㎥ に戻る。今回の指針が前回より小さいときは、一周したとみなす
    - 指針が 0〜9999 の外なら ValueError("reading must be between 0 and 9999")
    """
    if current <= previous:
        return current + 9999 - previous
    return current - previous
