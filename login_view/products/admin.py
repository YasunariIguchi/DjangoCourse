from django.contrib import admin
from .models import Product, Picture
from .forms import ProductForm, PictureUploadForm


class PictureInline(admin.TabularInline):
    model = Picture
    form = PictureUploadForm
    extra = 1  # 新規追加フォームの数


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    readonly_fields = ('create_at', 'update_at')
    inlines = [PictureInline]
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
