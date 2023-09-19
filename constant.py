from datetime import datetime
import re


def type_conversion_to_datetime(value: str) -> datetime:
    """str → datetimeに型変換する"""

    return datetime.strptime(value, "%Y-%m-%d %H:%M")


def is_null_or_empty(value):
    """Noneもしくは空の判定

    Args:
        value (str): Noneもしくは空であるかを確認する値
    Returns:
        bool: (例: Noneや空の場合はTrue、値が存在すればFalse)
    """

    if value is None:
        return True
    if len(value) == 0:
        return True
    if value == "":
        return True

    return False


def is_valid_datetime(value: str) -> bool:
    """指定した日時フォーマットかチェックする

    CSV取り込み時のValidationに使用する。
    """

    pattern = r"^\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}$"

    if re.match(pattern, value):
        return True

    return False
