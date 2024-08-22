# from django.shortcuts import render
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        query = super().get_queryset()
        product_name = self.request.GET.get("product_name", "")
        product_type_name = self.request.GET.get("product_type_name", "")
        price_order = self.request.GET.get("price_order", "")
        if product_name:
            query = query.filter(name__icontains=product_name)

        if product_type_name:
            query = query.filter(type__icontains=product_type_name)

        if price_order == "asc":
            query = query.order_by("price")
        elif price_order == "desc":
            query = query.order_by("-price")
        return query


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
