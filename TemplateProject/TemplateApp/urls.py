from django.urls import path
from . import views

app_name = 'template_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('ichiran/', views.ichiran, name='ichiran'),
    path('yourname/<sei>/<mei>/', views.yourname, name='yourname'),
]