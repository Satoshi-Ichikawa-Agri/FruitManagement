"""ローカル環境の設定"""
from .base import *


SECRET_KEY = (
    "django-insecure-qiptzex**gj0p3h=l@e0#+xhh#5#--)$n_4dvpxmw38(k7u_1)"
)
DEBUG = True
ALLOWED_HOSTS = []

# MySQL(Local-Server)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "fruit_management",
        "USER": "devsaichikawa",
        "PASSWORD": "Asagakita40813011",
        "HOST": "localhost",
        "PORT": "3306",
        "ATOMIC_REQUESTS": True,
    }
}
