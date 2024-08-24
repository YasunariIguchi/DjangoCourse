from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from .models import Product, Cart, CartItem, Address, Picture, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from .forms import CartItemForm, AddressForm
from django.core.cache import cache
from django.db import transaction


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
        context["is_added"] = CartItem.objects.filter(
            product=context["product"],
            cart=Cart.objects.filter(user=self.request.user).first(),
        ).exists()
        return context


@login_required
def add_product(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
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
                quantity=quantity, product_id=product_id, cart=cart[0]
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
        context["address"] = cache.get(f"address_user_{self.request.user.id}")

        return context


class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    template_name = "cartitem_update.html"
    form_class = CartItemForm

    def get_success_url(self) -> str:
        # print(self.get_object)
        return reverse_lazy("products:cartitem_list")


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = "cartitem_delete.html"

    def get_success_url(self) -> str:
        # print(self.get_object)
        return reverse_lazy("products:cartitem_list")


class InputAddressView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = "input_address.html"
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = cache.get(f"address_user_{self.request.user.id}")
        if address:
            context["form"].fields["zip_code"].initial = address.zip_code
            context["form"].fields["prefecture"].initial = address.prefecture
            context["form"].fields["address"].initial = address.address
            context["cached_address_id"] = address.id
        address_options = Address.objects.filter(user=self.request.user).all()
        context["address_options"] = address_options
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # ログイン中のユーザーを設定
        return super().form_valid(form)

    def get_success_url(self) -> str:
        # print(self.get_object)
        return reverse_lazy("products:confirm_order")

    def get(self, request, *args, **kwargs):
        if not self.request.user.cart.cartitem_set.exists():
            raise Http404("商品が入っていませんお")
        return super().get(request, *args, **kwargs)


@login_required
@require_POST
def change_address(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        address_id = request.POST.get("address_id")
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            response_data = {
                "zip_code": address.zip_code,
                "prefecture": address.prefecture,
                "address": address.address,
            }
            return JsonResponse(response_data)
        except Address.DoesNotExist:
            return JsonResponse({"message": "住所が見つかりませんでした"}, status=404)
    return JsonResponse({"message": "無効なリクエストです"}, status=400)


class ConfirmOrderView(LoginRequiredMixin, TemplateView):
    template_name = "confirm_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user_id=self.request.user.id)
        context["cart"] = cart
        # cartitem_list = CartItem.objects.filter(cart__user=self.request.user)
        # context["cartitem_list"] = cartitem_list
        address = cache.get(f"address_user_{self.request.user.id}")
        context["address"] = address
        total_price = 0
        items = []
        for item in cart.cartitem_set.all():
            total_price += item.product.price * item.quantity
            picture = item.product.picture_set.first()
            picture = picture.picture if picture else None
            tmp_item = {
                "id": item.id,
                "picture": picture,
                "name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                }
            items.append(tmp_item)
        context["items"] = items
        context["total_price"] = total_price

        self.request.session['total_price'] = total_price
        self.request.session['address_id'] = address.id

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        total_price = self.request.session.get('total_price', 0)
        address_id = self.request.session.get('address_id', "")
        order = Order(
            user=request.user,
            address_id=address_id,
            total_price=total_price
        )
        order.save()

        for cart_item in request.user.cart.cartitem_set.all():
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise Http404("注文処理でエラーが発生しました。")
            product.stock -= cart_item.quantity
            product.save()
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            order_item.save()
            cart_item.delete()

        del self.request.session['total_price']
        del self.request.session['address_id']

        return redirect('products:product_list')
