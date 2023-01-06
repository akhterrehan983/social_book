from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    address = models.CharField(max_length=300)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


from django.db import models

class file(models.Model):
    upload_to = models.FileField()
    email = models.CharField(max_length=100)


# Create your models here.


# class userDetails(models.Model):
#     email = models.CharField(max_length = 200)
#     password = models.CharField(max_length = 200)

