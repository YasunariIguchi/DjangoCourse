from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.dispatch import receiver
import os
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
        
class Book(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    
    class Meta:
        db_table = "books"
    
    def get_absolute_url(self):
        return reverse_lazy("store:detail_book", kwargs={"pk": self.pk})


class PictureManager(models.Manager):
    def filter_by_book(self, book):
        return self.filter(book=book).all()

class Picture(BaseModel):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    picture = models.FileField(upload_to="picture")
    objects = PictureManager()
    
    class Meta:
        db_table = "pictures"

@receiver(models.signals.post_delete, sender=Picture)
def delete_picture(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)