from django.urls import path
from . import views

app_name = "form_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("form_page/", views.form_page, name="form_page"),
    path("form_post/", views.form_post, name="form_post"),
    path("upload_sample/", views.upload_sample, name="upload_sample"),
    path("upload_model_form/", views.upload_model_form, name="uploads_model_form"),
    path("student_list/", views.student_list, name="student_list"),
    path("student_create/", views.student_create, name="student_create"),
    path("student_update/<int:id>", views.student_update, name="student_update"),
    path("student_delete/<int:id>", views.student_delete, name="student_delete"),
    path("student_set_form/", views.student_set_form, name="student_set_form"),
]