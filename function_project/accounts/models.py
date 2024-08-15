from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to="picture/")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = UserManager()
    
    class Meta:
        db_table = "users"

class UserActivateTokensManager(models.Manager):
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(token=token, expired__gte=timezone.now()).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired = models.DateTimeField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "user_activate_tokens"
        
    objects = UserActivateTokensManager()
        
@receiver(post_save, sender=User)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens.objects.create(
        user=instance,
        token=str(uuid4()),
        expired=timezone.now() + timedelta(days=1)
    )
    print(f"http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}")