from django.contrib.auth.models import User
from django.db import models

from website.libs.const import Visibility, Thumb
from website.libs.model_utils import get_profile_by_user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=140, default="")
    picture_url = models.CharField(max_length=256, default=None, blank=True, null=True)


class Post(models.Model):
    # Post is also Comment... Since Comment has same architecture as Post, so it can create posts under post.
    main_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, default=None)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=340)
    date = models.DateTimeField(auto_now=True)
    visibility = models.PositiveSmallIntegerField(
        default=Visibility.PUBLIC)  # 0: public, 1: friends, 2: myself; TODO: show posts only by visibility attribute.

    def __str__(self):
        return self.content[:40]

    def get_thumbs_up(self):
        return len(Reaction.objects.all().filter(post=self, value=0))

    def get_thumbs_down(self):
        return len(Reaction.objects.all().filter(post=self, value=1))

    def get_thumb_value(self, user):
        profile = get_profile_by_user(user)
        if profile is None:
            raise ValueError("User must be user type or profile type.")

        try:
            reaction = Reaction.objects.get(post=self, author=profile)
            return reaction.value
        except ValueError:
            return -1

    def get_message_count(self):
        return len(Post.objects.all().filter(main_post=self))


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=Thumb.UP)
    date = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=340)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
