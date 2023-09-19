from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.urls import reverse_lazy

from .mixin import BaseMixin


class UserManager(BaseUserManager):
    """User操作用クラス"""

    def create_user(self, email, password=None):
        """一般ユーザーの作成処理"""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Superユーザーの作成処理"""
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseMixin, AbstractBaseUser, PermissionsMixin):
    """User"""

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    is_staff = models.BooleanField(default=False)  # 管理者フラグ

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Trueをリターンして権限があることを知らせます。
        Objectをリターンする場合当該Objectで使う権限があるかどうか確認する手続きが必要です。
        """
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Trueをリターンしてアプリ(App)のモデル(Model)へ接続できるようにします。
        """
        "Does the user have permits to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse_lazy("home")
