from django.db import models
from django.contrib.auth.models import AbstractUser,User
# Create your models here.

# class User(AbstractUser):

class Post(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=10000)
    content = models.CharField(max_length=10000)
    creation_date = models.DateField()

class Like(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    post = models.ForeignKey(Post,on_delete=models.SET_NULL,null=True)
    likes_dislike = models.BooleanField(null=True,blank = True)