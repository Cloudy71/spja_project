from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    context = {
        "posts": Post.objects.select_related("author").order_by("-date"),
        "logged_user": request.user if request.user.is_authenticated else None,
    }
    return render(request, "website/timeline.html", context)


def profile(request, login):
    context = {
        "profile": get_object_or_404(Profile, user__username=login),
        "posts": Post.objects.filter(author__user__username=login).order_by("-date"),
        "logged_user": request.user if request.user.is_authenticated else None,
    }
    return render(request, "website/profile.html", context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["login"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, "website/log_in.html", {"form": LoginForm})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

def sign_in(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            
            user = User.objects.create_user(
                username = form.cleaned_data["login"],
                last_name = form.cleaned_data["lastName"],
                first_name = form.cleaned_data["firstName"],
                password = form.cleaned_data["password"]
            )
            Profile.objects.create(description = form.cleaned_data["description"], user=user)
    return render(request, "website/sign_in.html", {"form": UserForm()})

@login_required
def post(request):
    if request.method == "POST":
        text = request.POST["text"]
        Post.objects.create(author=get_object_or_404(Profile, user=request.user), content=text)
    return redirect("/")