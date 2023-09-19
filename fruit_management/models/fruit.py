from django.db import models

from .mixin import BaseMixin


class Fruit(BaseMixin):
    """果物マスタテーブル"""

    name = models.CharField(max_length=100)  # 果物名称
    price = models.PositiveIntegerField()  # 単価

    class Meta:
        db_table = "fruit"

    def __str__(self):
        return self.name


class Sales(BaseMixin):
    """販売情報テーブル"""

    fruit_name = models.CharField(max_length=100)  # 販売した果物名称
    quantity = models.PositiveIntegerField()  # 個数
    sales = models.PositiveIntegerField()  # 売上
    sales_date = models.DateTimeField()  # 販売日

    class Meta:
        db_table = "sales"

    def __str__(self):
        return self.fruit_name
