from django.shortcuts import render, get_object_or_404
from .models import SocialUser, Post
# Create your views here.

def index(request):

    context = {
        "posts": Post.objects.select_related("author").order_by("-date")
    }
    print(context)
    return render(request, "website/timeline.html", context)

def profile(request, login):
    context = {
        "profile": get_object_or_404(SocialUser, username=login),
        "posts": Post.objects.filter(author__username=login).order_by("-date")
    }
    return render(request, "website/profile.html", context)