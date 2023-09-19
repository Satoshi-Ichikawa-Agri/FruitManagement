from django.db import models


class BaseMixin(models.Model):
    """Base Mixin"""

    created_at = models.DateTimeField(auto_now_add=True)  # 作成日
    updated_at = models.DateTimeField(auto_now=True)  # 更新日

    class Meta:
        abstract = True
