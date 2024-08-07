from django.shortcuts import render
from . import forms
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
    return render(request, "formapp/form_page.html", {"form": form})