from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import os
from accounts.models import User

# Create your models here.


class BaseModel(models.Model):
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_at = timezone.now()
        self.update_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Product(BaseModel):
    PRODUCT_TYPES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
        ('type4', 'Type 4'),
        ('type5', 'Type 5'),
        ('type6', 'Type 6'),
        ('type7', 'Type 7'),
        ('type8', 'Type 8'),
        ('type9', 'Type 9'),
        ('type10', 'Type 10'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    producer = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    class Meta:
        db_table = "products"

    def clean(self):
        if self.producer and not self.producer.is_staff:
            raise ValidationError("Producer must be a staff member.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class PictureManager(models.Manager):
    def filter_by_product(self, product):
        return self.filter(product=product).all()


class Picture(BaseModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    picture = models.FileField(upload_to="picture")
    objects = PictureManager()

    class Meta:
        db_table = "pictures"


@receiver(models.signals.post_delete, sender=Picture)
def delete_picture(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        db_table = "carts"


class CartItemManager(models.Manager):
    def save_item(self, quantity, product_id, cart):
        c = self.model(quantity=quantity, product_id=product_id, cart=cart)
        c.save()


class CartItem(models.Model):
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    objects = CartItemManager()

    class Meta:
        db_table = "cart_items"
        unique_together = [["product", "cart"]]


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    zip_code = models.CharField(max_length=8)
    prefecture = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

    class Meta:
        db_table = "addresses"
        unique_together = ["user", "zip_code", "prefecture", "address", ]

    def __str__(self) -> str:
        return f"{self.zip_code} {self.prefecture} {self.address}"