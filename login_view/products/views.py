from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

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
        context["is_added"] = CartItem.objects.filter(product=context["product"], cart=Cart.objects.filter(user=self.request.user).first()).exists()
        return context


@login_required
def add_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        product = get_object_or_404(Product, id=product_id)
        if int(quantity) > product.stock:
            response = JsonResponse({"message": "在庫数を超えています"})
            response.status_code = 403
            return response
        if int(quantity) <= 0:
            response = JsonResponse({"message": "在庫数は1以上を入力してください"})
            response.status_code = 403
            return response
        cart = Cart.objects.get_or_create(user=request.user)
        if all([product_id, cart, quantity]):
            CartItem.objects.save_item(
                quantity=quantity,
                product_id=product_id,
                cart=cart[0]
            )
            return JsonResponse({"message": "商品をカートに追加しました。"})


class CartItemListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cartitem_list.html"

    def get_queryset(self):
        query = super().get_queryset()
        query.filter(cart=Cart.objects.get(user=self.request.user))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.get_queryset()
        total_price = 0
        items = []
        for q in query:
            total_price += q.quantity * q.product.price
            picture = q.product.picture_set.first()
            picture = picture.picture if picture else None
            in_stock = True if q.quantity <= q.product.stock else False
            tmp_item = {
                "quantity": q.quantity,
                "picture": picture,
                "name": q.product.name,
                "id": q.id,
                "price": q.product.price,
                "in_stock": in_stock,
            }
            items.append(tmp_item)
        context["items"] = items
        context["total_price"] = total_price

        return context
