from django.urls import path
from . import views

app_name = 'first_app'
urlpatterns = [
    path('url_xx', views.index, name='index'),
    path('add/<int:num1>/<int:num2>', views.add, name='add'),
]