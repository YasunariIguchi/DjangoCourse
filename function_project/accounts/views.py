from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens

# Create your views here.
def home(request):
    return render(request, "accounts/home.html")

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect("accounts:home")
            # user = regist_form.save(commit=False)
            # user.set_password(user.cleaned_data["password"])
            # user.save()
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(request, "accounts/regist.html", context={
        "regist_form": regist_form
    })
    
def activate_user(request, token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request, "accounts/activate_user.html"
    )