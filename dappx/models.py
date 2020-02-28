# dappx/models.py

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE)

def __str__(self):
  return self.user.username


class Post(models.Model):
    uploadfile = models.FileField(null=True,blank=True,upload_to='Files')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
