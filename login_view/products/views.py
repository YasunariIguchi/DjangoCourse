# from django.shortcuts import render
# Create your views here.
from django.views.generic.list import ListView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        qs = super().get_queryset().order_by("-price")
        return qs
