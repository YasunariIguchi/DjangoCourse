from django import forms
from .models import Product, Picture
from accounts.models import User
from datetime import datetime


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
