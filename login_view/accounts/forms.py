from typing import Any
from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm


class RegistForm(forms.ModelForm):
    username = forms.CharField(label="名前")
    age = forms.IntegerField(label="年齢", min_value=0)
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "age", "email", "password"]

    def save(self, commit: bool = True) -> Any:
        password = self.cleaned_data["password"]
        validate_password(password, self.instance)
        self.instance.set_password(password)
        return super().save(commit=commit)


# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label="メールアドレス")
#     password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    remember = forms.BooleanField(label="ログイン状態を保持する", required=False)
