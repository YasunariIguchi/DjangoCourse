from django.shortcuts import render, Http404
from datetime import datetime
import os

class Member:
    def __init__(self, id, name, img, entry_date):
        self.id = id
        self.name = name
        self.img = img
        self.entry_date = entry_date

    def get_membership_duration(self):
        now = datetime.now()
        duration = now - self.entry_date
        years = duration.days // 365
        months = (duration.days % 365) // 30
        return years, months
def image_path(filename):
    return os.path.join("img", filename)

taro = Member(1, "Taro", image_path("taro.jpg"), datetime(2020, 1, 1))
jiro = Member(2, "Jiro", image_path("jiro.jpg"), datetime(2020, 4, 1))
hanako = Member(3, "Hanako", image_path("hanako.jpg"), datetime(2021, 12, 31))
yoshiko = Member(4, "Yoshiko", image_path("yoshiko.jpg"), datetime(2024, 4, 1))
members_list = [taro, jiro, hanako, yoshiko]
# Create your views here.
def home(request):
    return render(request, "home.html")

def members(request):
    return render(request, "members.html", {"members": members_list} )



def member(request, id):
    member = next((m for m in members_list if m.id == id), None)
    if member is None:
        raise Http404("Member does not exist")
    years, months = member.get_membership_duration()
    return render(request, "member.html", {"member": member, "years": years, "months": months} )