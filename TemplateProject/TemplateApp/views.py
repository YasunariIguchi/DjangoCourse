from django.shortcuts import render

from django.http import HttpResponse

class Ramen:
    def __init__(self, men, soup):
        self.men = men
        self.soup = soup
    
# Create your views here.
def index(request):
    val = [1,2,3,4,5]
    return render(request, 'TemplateApp/index.html', context={'value': val})

def ichiran(request):
    instance = Ramen('hoso', 'tonkotu')
    return render(request, 'TemplateApp/ichiran.html', {'ramen': instance})

def yourname(request, sei, mei):
    return HttpResponse(f'<h1>yourname: {sei} {mei}</h1>')