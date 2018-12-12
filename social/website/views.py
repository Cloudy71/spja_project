from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from website.lib.model_utils import is_user_followed_by, get_profile_by_user
from .models import Profile, Post, Follow
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        context = {
            "is_logged": True if request.user.is_authenticated else False,
        }
        rndr = "website/index.html"
    else:
        context = {
            "posts": Post.objects.select_related("author").order_by("-date")[:10],
            "logged_user": Profile.objects.get(user=request.user) if request.user.is_authenticated else None,
        }
        rndr = "website/timeline.html"

    return render(request, rndr, context)


def profile(request, login):
    if not request.user.is_authenticated:
        return index(request)

    context = {
        "profile": get_object_or_404(Profile, user__username=login),
        "posts": Post.objects.filter(author__user__username=login).order_by("-date")[:10],
        "logged_user": Profile.objects.get(user=request.user) if request.user.is_authenticated else None,
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
            else:
                return index(request)
    return render(request, "website/log_in.html", {"form": LoginForm})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["login"],
                last_name=form.cleaned_data["lastName"],
                first_name=form.cleaned_data["firstName"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"]
            )
            Profile.objects.create(user=user)
            return index(request)

    return render(request, "website/sign_up.html", {"form": UserForm()})


@login_required
def post(request):
    if request.method == "POST":
        text = request.POST["text"]
        Post.objects.create(author=get_object_or_404(Profile, user=request.user), content=text)
    return redirect("/")


def follow(request, login):
    if len(login) == 0:
        return HttpResponse("0")
    login_user = User.objects.get(username=login)
    if not is_user_followed_by(login_user, request.user):
        Follow.objects.create(follower=get_profile_by_user(request.user), following=get_profile_by_user(login_user))
        return HttpResponse("1")
        pass
    return HttpResponse("0")
    pass


def unfollow(request, login):
    if len(login) == 0:
        return HttpResponse("0")
    login_user = User.objects.get(username=login)
    if is_user_followed_by(login_user, request.user):
        Follow.objects.get(follower=get_profile_by_user(request.user),
                           following=get_profile_by_user(login_user)).delete()
        return HttpResponse("1")
        pass
    return HttpResponse("0")
    pass
