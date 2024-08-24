from typing import Any
from django import forms
from .models import Product, Picture, CartItem, Address
from accounts.models import User
from datetime import datetime
from django.core.cache import cache
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['create_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producer'].queryset = User.objects.filter(is_staff=True)


class PictureUploadForm(forms.ModelForm):
    picture = forms.FileField(required=False)

    class Meta:
        model = Picture
        fields = ["picture",]

    def save(self, *args, **kwargs):
        obj = super().save(commit=False)
        if not obj.pk:
            obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        # obj.product = kwargs.get("product")
        obj.save()
        return obj


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("数量は1以上でなければなりません。")
        if quantity > self.instance.product.stock:
            raise forms.ValidationError("在庫数を超えた数量の注文はできません。")
        return quantity


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        labels = {
            "zip_code": "郵便番号",
            "prefecture": "都道府県",
            "address": "住所詳細"
        }

    def save(self) -> Any:
        address_data = self.cleaned_data
        try:
            address = Address.objects.get(
                user=self.instance.user,
                zip_code=address_data['zip_code'],
                prefecture=address_data['prefecture'],
                address=address_data['address']
            )
        except Address.DoesNotExist:
            address = Address.objects.create(user=self.instance.user, **address_data)

        cache.set(f'address_user_{address.user.id}', address)
        return address
