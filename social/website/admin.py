from django.contrib import admin
from .models import SocialUser, Post, Comment

# Register your models here.

admin.site.register(SocialUser)
admin.site.register(Post)
admin.site.register(Comment)
