from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=140)


class Reaction(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=340)
    date = models.DateTimeField(auto_now=True)
    reactions = models.ManyToManyField(Reaction)

    def get_thumbs(self):
        thumbs = [0, 0]
        for reaction in self.reactions.all():
            thumbs[reaction.value] += 1
            pass

        return thumbs
        pass


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    reactions = models.ManyToManyField(Reaction)
