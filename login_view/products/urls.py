from django.urls import path
from .views import ProductListView, ProductDetailView, CartItemUpdateView, \
    add_product, CartItemListView, CartItemDeleteView, InputAddressView, \
    change_address

app_name = "products"

urlpatterns = [
    path("product_list/", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>", ProductDetailView.as_view(),
         name="product_detail"),
    path("add_product/", add_product, name="add_product"),
    path("cartitem_list/", CartItemListView.as_view(), name="cartitem_list"),
    path("cartitem_update/<int:pk>", CartItemUpdateView.as_view(), name="cartitem_update"),
    path("cartitem_delete/<int:pk>", CartItemDeleteView.as_view(), name="cartitem_delete"),
    path("input_address/", InputAddressView.as_view(), name="input_address"),
    path("change_address/", change_address, name="change_address"),
]
