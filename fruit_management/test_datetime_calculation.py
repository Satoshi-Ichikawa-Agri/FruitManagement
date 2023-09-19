"""fruit_management.views.datetime_calculation.pyのPytest"""
from datetime import datetime
import pytest

from fruit_management.views.datetime_calculation import (
    get_datetime_in_designated_range,
    get_time_in_designated_range,
)


@pytest.mark.django_db
def test_get_datetime_in_designated_range():
    start_date, end_date = get_datetime_in_designated_range(True)
    assert start_date == datetime(2023, 9, 1, 0, 0, 0)
    assert end_date == datetime(2023, 9, 30, 23, 59, 59)
