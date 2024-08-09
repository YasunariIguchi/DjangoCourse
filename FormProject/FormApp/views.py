from django.shortcuts import render
from . import forms
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def index(request):
    return render(request, "formapp/index.html")

def form_page(request):
    form = forms.UserInfo()
    if request.method == "POST":
        form = forms.UserInfo(request.POST)
        if form.is_valid():
            print("validation成功")
            # print(
            #     f"name: {form.cleaned_data["name"]}, mail: {form.cleaned_data["mail"]}, age: {form.cleaned_data["age"]}"
            # )
            print(form.cleaned_data)
        else:
            print("dame")
            print(form.errors)
    return render(request, "formapp/form_page.html", {"form": form})

def form_post(request):
    form = forms.PostModelForm()
    if request.method == 'POST':
        form = forms.PostModelForm(request.POST)
        if form.is_valid():
            print("validation成功")
            form.save()
            print(form.cleaned_data)
            
    return render(request, "formapp/form_post.html", {"form": form})

def upload_sample(request):
    if request.method == "POST" and request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage()
        file_path = os.path.join("upload", upload_file.name)
        file = fs.save(file_path, upload_file)
        uploaded_file_url = fs.url(file)
        return render(request, 'formapp/upload_file.html', {
            'uploaded_file_url': uploaded_file_url})
    return render(request, "formapp/upload_file.html")


def upload_model_form(request):
    user = None
    if request.method == "POST":
           form = forms.UserForm(request.POST, request.FILES)
           if form.is_valid():
               user = form.save()
    else:
        form = forms.UserForm()
    return render(request, "formapp/upload_model_form.html", {"form": form, "user": user})