from django.shortcuts import render, redirect, get_object_or_404
from .models import Item

# Create your views here.

def item_list(request):
    items = Item.objects.all()
    return render(request, "store/item_list.html", context={
        "items": items,
    })
    
def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    return render (request, "store/item_detail.html", context={
        "item": item,
    })
    
def to_google(request):
    return redirect("https://www.google.com")

def one_item(request):
    return redirect("store:item_detail", id=1)