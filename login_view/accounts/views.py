from typing import Any
from django import http
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy

from datetime import datetime

from .models import User
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class RegistUserView(CreateView):
    template_name = "regist.html"
    form_class = RegistForm


# class UserLoginView(FormView):
#     template_name = "user_login.html"
#     form_class = UserLoginForm

#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         form = self.get_form()
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             next_url = request.POST["next"]
#             if user is not None and user.is_active:
#                 login(request, user)
#             if next_url:
#                 return redirect(
#                     next_url
#                 )  # Assuming 'home'
#             return redirect(
#                 "accounts:home"
#             )  # Assuming 'home' is the name of the home URL pattern
#         return self.form_invalid(form)
class UserLoginView(LoginView):
    template_name = "user_login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        remember = form.cleaned_data["remember"]
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)


# class UserLogoutView(View):
#     def get(self, request: HttpRequest, *args: str, **kwargs: Any):
#         logout(request)
#         return redirect("accounts:user_login")
class UserLogoutView(LogoutView):
    pass


# @method_decorator(login_required, name='dispatch')
class UserView(LoginRequiredMixin, TemplateView):
    template_name = "user.html"

    # @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)