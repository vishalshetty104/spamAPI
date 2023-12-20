import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

# Create your models here.

class User(AbstractUser):

    phone = models.BigIntegerField(unique=True, error_messages={"unique":"Phone number already exists"})

    username = models.CharField(max_length=100)

    email = models.EmailField(max_length=200, blank=True)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def check_password(self, raw_password):
        return super().check_password(raw_password)

    def __str__(self):
        return self.username

class GlobalDb(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    name = models.CharField(max_length=100)

    phone_no = models.CharField(max_length=10, blank=False)

    email = models.EmailField(max_length=200,blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True) #this number is in which user's contact list

    is_registered = models.BooleanField(default=False)

    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" "+str(self.id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL) #generates token for user after registration
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
