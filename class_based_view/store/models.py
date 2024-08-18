from django.db import models
from django.urls import reverse_lazy

# Create your models here.

class BaseModel(models.Model):
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()
    
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