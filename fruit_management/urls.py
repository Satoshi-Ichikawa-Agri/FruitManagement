from django.urls import path

from fruit_management.views.accounts_views import (
    SignUpView,
    UserLoginView,
    UserLogoutView,
    HomeView,
)
from fruit_management.views.fruit_management_views import (
    FruitListView,
    FruitRegisterView,
    FruitEditView,
    fruit_delete,
)
from fruit_management.views.sales_management_views import (
    sales_list,
    sales_register,
    sales_edit,
    sales_delete,
)
from fruit_management.views.sales_statistics_views import statistics_summary


urlpatterns = [
    # account
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # Fruit
    path("index/", FruitListView.as_view(), name="index"),
    path("register/", FruitRegisterView.as_view(), name="register"),
    path("edit/<int:pk>/", FruitEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", fruit_delete, name="delete"),
    # Sales
    path("sales_index/", sales_list, name="sales_index"),
    path("sales_register/", sales_register, name="sales_register"),
    path("sales_edit/<int:pk>/", sales_edit, name="sales_edit"),
    path("sales_delete/<int:pk>/", sales_delete, name="sales_delete"),
    # Statistics
    path("sales_statistics/", statistics_summary, name="sales_statistics"),
]
