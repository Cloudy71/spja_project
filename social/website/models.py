from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SocialUser(User):
    description = models.CharField(max_length=140)

class Post(models.Model):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=340)
    date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    