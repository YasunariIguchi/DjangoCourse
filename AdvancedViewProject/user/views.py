from django.shortcuts import render
from .forms import UserForm, ProfileForm

# Create your views here.

def user_list(request):
    return render(request, "user/user_list.html")

def index(request):
    return render(request, "user/index.html")

def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILE or None)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
    
    return render(request, "user/registration.html", context={
        "user_form": user_form,
        "profile_form": profile_form,
    })
        
    