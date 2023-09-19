from django.contrib import admin

from fruit_management.models.accounts_models import User
from fruit_management.models.fruit import Fruit, Sales


admin.site.register(User)
admin.site.register(Fruit)
admin.site.register(Sales)
