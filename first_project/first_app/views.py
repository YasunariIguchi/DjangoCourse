from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('<h1>Something</h1>')

def add(request, num1, num2):
    sum = num1 + num2
    return HttpResponse(f'<h1>sum = {sum}</h1>')