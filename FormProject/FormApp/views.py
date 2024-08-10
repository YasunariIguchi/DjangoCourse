from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from . import forms
from .models import Student
from django.core.files.storage import FileSystemStorage
import os
from django.shortcuts import get_object_or_404
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


def student_list(request):
    students = Student.objects.all()
    return render(request, "formapp/student_list.html", {"students": students})

def student_create(request):
    student = None
    if request.method == "POST":
           form = forms.StudentForm(request.POST, request.FILES)
           if form.is_valid():
               student = form.save()
               messages.success(request, f"新たな学生 {student.name} を作成しました。")
               return redirect('form_app:student_list')
    else:
        form = forms.StudentForm(initial={
            "name":"ossan",
            "age":"31",
            "grade":"6",
        })
    return render(request, "formapp/student_form.html", {"form": form, "student": student})

def student_update(request, id):
    student = Student.objects.get(id=id)
    update_form = forms.StudentForm(instance=student)
    if request.method == "POST":
        update_form =  forms.StudentForm(request.POST, request.FILES, instance=student)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, f"学生 {student.name} を更新しました。")
            return redirect('form_app:student_list')
    return render(request, "formapp/student_update.html", {"update_form": update_form, "id": id})

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        messages.success(request, f"学生 {student.name} を削除しました。")
        return redirect('form_app:student_list')
    return render(request, "formapp/student_delete.html", {"id": id, "name": student.name})

def student_set_form(request):
    # その1の方。forms.pyの関数は使ってない
    StudentFormSet = modelformset_factory(Student, fields='__all__', extra=3)
    formset = StudentFormSet(request.POST or None, request.FILES or None, queryset=Student.objects.none())
    if formset.is_valid():
        formset.save()
        if request.method == "POST":
            messages.success(request, f"おっさんを一括追加しました。")
            return redirect('form_app:student_list')
    return render(request, "formapp/student_set_form.html", {"formset": formset}) 