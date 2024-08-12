from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(label="名前")
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ("username", "email", "password")
        
class ProfileForm(forms.ModelForm):
    website = forms.URLField(label="ホームページ")
    picture = forms.FileField(label="写真")
    class Meta():
        model = Profile
        fields = ("website", "picture")