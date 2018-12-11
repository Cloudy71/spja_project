from django.contrib import admin

from website.models import Reaction, Follow
from .models import Profile, Post

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Follow)
