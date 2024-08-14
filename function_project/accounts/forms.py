from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegistForm(forms.ModelForm):
    username = forms.CharField(label="名前")
    age = forms.IntegerField(label="年齢", min_value=0)
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="パスワード再入力", widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("username", "age", "email", "password")
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("パスワードが一致しないお")
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data["password"], user)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user