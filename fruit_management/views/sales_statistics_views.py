from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from fruit_management.models.fruit import Sales
from fruit_management.views.datetime_calculation import (
    get_datetime_in_designated_range,
    get_time_in_designated_range,
)


@login_required
def statistics_summary(request):
    """販売統計情報ページ用の統計処理"""

    template_name = "sales_statistics/statistics.html"
    sales_model_list = list(Sales.objects.all().values())

    cumulative_sales = 0  # 累計売上
    sales_current_month = 0  # 当月売上合計
    sales_a_month_ago = 0  # 前月売上合計
    sales_two_months_ago = 0  # 前々月売上合計

    sales_today = 0  # 本日売上合計
    sales_a_day_ago = 0  # 前日売上合計
    sales_two_days_ago = 0  # 前々日売上合計

    current_month_fruits_list = []  # 当月のSales集計
    a_month_ago_fruits_list = []  # 前月のSales集計
    two_months_ago_fruits_list = []  # 前々月のSales集計

    today_fruits_list = []  # 本日のSales集計
    a_day_ago_fruits_list = []  # 前日のSales集計
    two_days_ago_fruits_list = []  # 前々日のSales集計

    (
        first_day_of_current_month,
        last_day_of_current_month,
    ) = get_datetime_in_designated_range(
        True
    )  # 当月初日 + 当月末日
    (
        first_day_a_month_ago,
        last_day_a_months_ago,
    ) = get_datetime_in_designated_range(
        False
    )  # 1ヵ月前の初日 + 1ヵ月前の末日
    (
        first_day_two_months_ago,
        last_day_two_months_ago,
    ) = get_datetime_in_designated_range(
        False, 2
    )  # 2ヵ月前の初日 + 2ヵ月前の末日

    start_of_today, end_of_today = get_time_in_designated_range(
        True
    )  # 本日の開始終了時刻
    start_a_day_ago, end_a_day_ago = get_time_in_designated_range(
        False, 1
    )  # 昨日の開始終了時刻
    start_two_days_ago, end_two_days_ago = get_time_in_designated_range(
        False, 2
    )  # 一昨日の開始終了時刻

    for obj in sales_model_list:
        temp_dict_monthly = {}
        temp_dict_daily = {}
        fruit_name = obj["fruit_name"]
        quantity = obj["quantity"]
        sales = obj["sales"]
        sales_date = obj["sales_date"]
        # ===== 累計売上 =====
        cumulative_sales += sales
        # ===== 月別 ===============================
        # 前々月～当月までの3ヵ月間の売上を月毎に集計する
        if first_day_two_months_ago <= sales_date <= last_day_two_months_ago:
            # 前々月
            sales_two_months_ago += sales
            temp_dict_monthly["fruit_name"] = fruit_name
            temp_dict_monthly["quantity"] = quantity
            temp_dict_monthly["sales"] = sales
            two_months_ago_fruits_list.append(temp_dict_monthly)
        if first_day_a_month_ago <= sales_date <= last_day_a_months_ago:
            # 前月
            sales_a_month_ago += sales
            temp_dict_monthly["fruit_name"] = fruit_name
            temp_dict_monthly["quantity"] = quantity
            temp_dict_monthly["sales"] = sales
            a_month_ago_fruits_list.append(temp_dict_monthly)

        # 当月だけは日別集計処理も同時に実施する
        if (
            first_day_of_current_month
            <= sales_date
            <= last_day_of_current_month
        ):
            # 当月
            sales_current_month += sales
            temp_dict_monthly["fruit_name"] = fruit_name
            temp_dict_monthly["quantity"] = quantity
            temp_dict_monthly["sales"] = sales
            current_month_fruits_list.append(temp_dict_monthly)
            # ===== 日別 ===============================
            # 前々日～当日までの3日間の売上を日毎に集計する
            # 前々日
            if start_two_days_ago <= sales_date <= end_two_days_ago:
                sales_two_days_ago += sales
                temp_dict_daily["fruit_name"] = fruit_name
                temp_dict_daily["quantity"] = quantity
                temp_dict_daily["sales"] = sales
                two_days_ago_fruits_list.append(temp_dict_daily)
            # 前日
            if start_a_day_ago <= sales_date <= end_a_day_ago:
                sales_a_day_ago += sales
                temp_dict_daily["fruit_name"] = fruit_name
                temp_dict_daily["quantity"] = quantity
                temp_dict_daily["sales"] = sales
                a_day_ago_fruits_list.append(temp_dict_daily)
            # 本日
            if start_of_today <= sales_date <= end_of_today:
                sales_today += sales
                temp_dict_daily["fruit_name"] = fruit_name
                temp_dict_daily["quantity"] = quantity
                temp_dict_daily["sales"] = sales
                today_fruits_list.append(temp_dict_daily)

    context = {
        # 累計売上
        "cumulative_sales": cumulative_sales,
        # 月別
        # 売上
        "sales_two_months_ago": sales_two_months_ago,
        "sales_a_month_ago": sales_a_month_ago,
        "sales_current_month": sales_current_month,
        # 月
        "first_day_of_current_month": first_day_of_current_month.strftime(
            "%Y/%#m"
        ),
        "first_day_a_month_ago": first_day_a_month_ago.strftime("%Y/%#m"),
        "first_day_two_months_ago": first_day_two_months_ago.strftime(
            "%Y/%#m"
        ),
        # Salesの詳細
        "two_months_ago_fruits_list": two_months_ago_fruits_list,
        "a_month_ago_fruits_list": a_month_ago_fruits_list,
        "current_month_fruits_list": current_month_fruits_list,
        # 日別
        # 売上
        "sales_two_days_ago": sales_two_days_ago,
        "sales_a_day_ago": sales_a_day_ago,
        "sales_today": sales_today,
        # 日
        "start_of_today": start_of_today.strftime("%Y/%#m/%#d"),
        "start_a_day_ago": start_a_day_ago.strftime("%Y/%#m/%#d"),
        "start_two_days_ago": start_two_days_ago.strftime("%Y/%#m/%#d"),
        # Salesの詳細
        "two_days_ago_fruits_list": two_days_ago_fruits_list,
        "a_day_ago_fruits_list": a_day_ago_fruits_list,
        "today_fruits_list": today_fruits_list,
    }

    return render(request, template_name, context)
