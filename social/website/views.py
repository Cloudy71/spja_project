from django.shortcuts import render
from .models import Post
# Create your views here.

def index(request):

    context = {
        "posts": Post.objects.select_related("author").order_by("date")
    }
    print(context)
    return render(request, "website/index.html", context)
