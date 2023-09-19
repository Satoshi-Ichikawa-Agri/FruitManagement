"""全体TODO

    ・Testコードの作成(Pytest)
"""
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


def get_current_datetime() -> datetime:
    """処理実行時点から見た、現在日時を取得する"""

    return datetime.now()


def get_datetime_in_designated_range(curr_or_ago, ago=1):
    """当月～指定月前の初日＆末日を取得する

    Args:
        curr_or_ago (bool): 当月か先月の判定フラグ (例: 当月:True, 先月以前: False)
        ago (int): 1~の10進数で受け取り、関数内で日数を計算する。
    Returns:
        datetime: (例:本日が「2023-09-15」であった場合、「2023-09-01」と「2023-09-30」を取得する)
    ToDo:
        2月～4月の時の挙動を調整する
    """

    current_date = get_current_datetime()
    ago_num = 0  # (例: ago=1なら1ヵ月前を指し、30*1=>30で計算を実施する)

    if curr_or_ago:
        # 当月初日
        start_date = current_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        # 当月末日
        a_month_later = current_date + timedelta(days=31)  # 1ヵ月後に移動
        end_date = a_month_later.replace(
            day=1, hour=23, minute=59, second=59
        ) - timedelta(days=1)
    else:
        # 先月初日
        ago_num = ago * 30
        a_month_ago = current_date - timedelta(days=ago_num)  # 〇ヵ月前に移動
        start_date = a_month_ago.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        if ago > 1:
            # 2ヵ月前以前の末日
            ago_num = (ago - 1) * 30
            tmp_date = current_date - timedelta(days=ago_num)  # 〇ヵ月前に移動
            end_date = tmp_date.replace(
                day=1, hour=23, minute=59, second=59
            ) - timedelta(days=1)
        else:
            # 1ヵ月の末日
            end_date = current_date.replace(
                day=1, hour=23, minute=59, second=59
            ) - timedelta(days=1)

    return make_aware(start_date), make_aware(end_date)


def get_time_in_designated_range(curr_or_ago, ago=0):
    """当日～2日前の開始時刻&終了時刻を取得する

    Args:
        curr_or_ago (bool): 本日か昨日以前の判定フラグ (例: 本日:True, 昨日以前: False)
        ago (int): 1~の10進数で受け取り、関数内で日数を計算する。
    Returns:
        datetime: (例:本日が「2023-09-16」であった場合、
                    「2023-09-16 00:00:00」と「2023-09-16 23:59:59」を取得する)
    """

    current_date = get_current_datetime()

    if curr_or_ago:
        # 本日開始時刻
        start_time = current_date.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        # 本日終了時刻
        end_time = current_date.replace(hour=23, minute=59, second=59)
    else:
        # 先日開始時刻
        any_days_ago = current_date - timedelta(days=ago)  # 〇日前に移動
        start_time = any_days_ago.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        # 先日終了時刻
        end_time = any_days_ago.replace(hour=23, minute=59, second=59)

    return make_aware(start_time), make_aware(end_time)
