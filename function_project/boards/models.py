from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.

class ThemeManager(models.Manager):
    def fetch_all_themes(self):
        return self.order_by('id').all()

class Theme(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    
    objects = ThemeManager()
    
    class Meta:
        db_table = "themes"
        

class CommentManager(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        theme = get_object_or_404(Theme, id=theme_id)
        return self.filter(theme=theme).order_by('id')


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    theme = models.ForeignKey("Theme", on_delete=models.CASCADE)
    
    objects = CommentManager()
    
    class Meta:
        db_table = "comments"