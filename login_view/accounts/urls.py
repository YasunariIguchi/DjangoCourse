from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("regist/", views.RegistUserView.as_view(), name="regist"),
    path("user_login/", views.UserLoginView.as_view(), name="user_login"),
    path("user_logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("user/", views.UserView.as_view(), name="user"),
]
