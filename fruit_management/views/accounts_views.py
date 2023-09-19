from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from fruit_management.forms import SignUpForm, UserLoginForm


class SignUpView(CreateView):
    """ユーザー登録処理"""

    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = "/login/"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """ログイン処理"""

    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """ログアウト処理"""

    pass


class HomeView(LoginRequiredMixin, TemplateView):
    """Home画面"""

    template_name = "home.html"
