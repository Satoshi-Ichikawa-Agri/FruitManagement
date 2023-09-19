from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from fruit_management.models.accounts_models import User
from fruit_management.models.fruit import Fruit, Sales


class SignUpForm(forms.ModelForm):
    """新規会員登録用の入力フォーム"""

    email = forms.EmailField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"placeholder": "sample@example.com"}),
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"placeholder": "半角英数字8文字以上"}),
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def are_similar(self, email, password):
        """emailとpasswordが似ているかを判定する"""
        email = email.lower()
        password = password.lower()

        # 文字列の一致率を計算
        match_rate = sum(c1 == c2 for c1, c2 in zip(email, password)) / max(
            len(email), len(password)
        )
        # 類似度の閾値や判定条件は適宜変更してください
        if match_rate >= 0.5:
            return True
        else:
            return False

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # emailとpasswordが似すぎている場合、エラーを出す
        if email and password:
            are_similar = self.are_similar(email, password)
            if are_similar:
                raise forms.ValidationError(
                    "このパスワードは email と似すぎています。",
                    code="password_similar_to_email",
                )

        # passwordが単純すぎる場合、エラーを出す
        try:
            user = super().save(commit=False)
            validate_password(self.cleaned_data["password"], user)
        except ValidationError:
            raise forms.ValidationError(
                "このパスワードは単純すぎる為、使用できません。", code="this_password_is_too_simple"
            )

        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user


class UserLoginForm(AuthenticationForm):
    """ログイン用のフォーム"""

    username = forms.EmailField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"placeholder": "sample@example.com"}),
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"placeholder": "半角英数字8文字以上"}),
    )


class FruitForm(forms.ModelForm):
    """果物登録フォーム"""

    name = forms.CharField(label="名称", max_length=100)  # 果物名称
    price = forms.IntegerField(label="単価")  # 単価

    class Meta:
        model = Fruit
        fields = ["name", "price"]


class SalesForm(forms.ModelForm):
    """販売登録フォーム"""

    choices = Fruit.objects.values_list("id", "name")

    fruit_name = forms.ChoiceField(label="果物", choices=choices)  # 販売した果物名称
    quantity = forms.IntegerField(label="個数")  # 個数
    sales_date = forms.DateTimeField(
        label="販売日時", input_formats="%Y-%m-%d %H:%M "
    )  # 販売日時

    class Meta:
        model = Sales
        fields = ["fruit_name", "quantity", "sales_date"]
