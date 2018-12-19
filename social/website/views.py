from json import dumps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from website.forms import ThumbForm, FollowForm, VisibilityForm, ChangeName, ChangePassword
from website.libs.const import Thumb, Visibility
from website.libs.model_utils import get_profile_by_user, post_exists, profile_exists_by_username, \
    reaction_exist, reaction_exist_value, follow_exist
from website.libs.views_utils import get_hashtags
from website.models import Reaction
from website.templatetags.timeline import get_profile_picture
from .forms import UserForm, LoginForm, ResponseForm
from .models import Profile, Post, Follow, Tag


def index(request):
    if not request.user.is_authenticated:
        context = {
            "is_logged": True if request.user.is_authenticated else False,
        }
        rndr = "website/index.html"
    else:
        # list(Follow.objects.filter(follower=logged_user).values("following"))
        # Case(
        #     When(Q(visibility=Visibility.MYSELF) & Q(author=logged_user),
        #          then=[Visibility.MYSELF, Visibility.FOLLOWERS, Visibility.PUBLIC]),
        #     When(Q(visibility=Visibility.FOLLOWERS) & Q(author=logged_user),
        #          then=[Visibility.FOLLOWERS, Visibility.PUBLIC])
        #     default=[Visibility.PUBLIC]
        # )
        logged_user = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
        context = {
            "posts": Post.objects.select_related("author").order_by("-date").filter(main_post=None).exclude(
                ~Q(author=logged_user), visibility=Visibility.MYSELF).exclude(
                Q(~Q(author__in=Follow.objects.filter(follower=logged_user).values("following")) & ~Q(
                    author=logged_user)), visibility=Visibility.FOLLOWERS)[:15],
            "logged_user": logged_user,
        }
        rndr = "website/timeline.html"

    return render(request, rndr, context)


def profile(request, login):
    if not request.user.is_authenticated:
        return index(request)

    logged_user = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {
        "profile": get_object_or_404(Profile, user__username=login),
        "posts": Post.objects.filter(author__user__username=login).order_by("-date").filter(main_post=None).exclude(
            ~Q(author=logged_user), visibility=Visibility.MYSELF).exclude(
            Q(~Q(author__in=Follow.objects.filter(follower=logged_user).values("following")) & ~Q(
                author=logged_user)), visibility=Visibility.FOLLOWERS)[:10],
        "logged_user": logged_user,
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
        post = Post.objects.create(author=get_object_or_404(Profile, user=request.user), content=text)
        Tag.objects.bulk_create([Tag(name=tag, post=post) for tag in get_hashtags(text)])
    return redirect("/")


@login_required
def follow(request):
    if request.method == "POST":
        form = FollowForm(request.POST)

        if form.is_valid() and form.cleaned_data["type"] in (0, 1) and profile_exists_by_username(
                form.cleaned_data["user"]):
            form_profile = get_profile_by_user(User.objects.get(username=form.cleaned_data["user"]))
            if form.cleaned_data["type"] == 1 and follow_exist(request.user, form_profile):
                Follow.objects.get(follower=get_profile_by_user(request.user), following=form_profile).delete()
            elif not follow_exist(request.user, form_profile):
                Follow.objects.create(follower=get_profile_by_user(request.user), following=form_profile)
            return HttpResponse("1")
        else:
            return HttpResponse("0")
    return HttpResponse("0")


@login_required
def thumb_give(request):
    if request.method == "POST":
        form = ThumbForm(request.POST)

        if form.is_valid() and form.cleaned_data["type"] in (-1, 0, 1) and post_exists(form.cleaned_data["post"]):
            this_post = Post.objects.get(id=form.cleaned_data["post"])
            this_profile = get_profile_by_user(request.user)

            if form.cleaned_data["type"] == -1 and reaction_exist(this_post, request.user):
                Reaction.objects.get(author=this_profile, post=this_post).delete()
                pass
            else:
                if reaction_exist(this_post, request.user):
                    react = Reaction.objects.get(post=this_post, author=this_profile)
                    react.value = form.cleaned_data["type"]
                    react.save()
                else:
                    Reaction.objects.create(post=this_post,
                                            author=this_profile,
                                            value=form.cleaned_data["type"])
            return HttpResponse(dumps({"up": len(Reaction.objects.filter(post=this_post, value=Thumb.UP)),
                                       "down": len(Reaction.objects.filter(post=this_post, value=Thumb.DOWN))}))
        else:
            return HttpResponse("0")
    return HttpResponse("0")


def tags(request, tag):
    logged_user = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    posts = [x.post.id for x in Tag.objects.filter(name=tag).select_related("post").order_by("-post__date")[:10]]
    show_posts = Post.objects.filter(id__in=posts).exclude(
        ~Q(author=logged_user), visibility=Visibility.MYSELF).exclude(
        Q(~Q(author__in=Follow.objects.filter(follower=logged_user).values("following")) & ~Q(
            author=logged_user)), visibility=Visibility.FOLLOWERS)
    context = {
        "posts": show_posts,
        "logged_user": logged_user,
    }
    return render(request, "website/timeline.html", context)


@login_required
def response(request):
    if request.POST:
        form = ResponseForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                main_post=get_object_or_404(Post, id=form.cleaned_data["main_post"]),
                author=get_object_or_404(Profile, user=request.user),
                content=form.cleaned_data["content"]
            )
            return HttpResponse(dumps({"login": request.user.username, "name": request.user.get_full_name(),
                                       "picture_url": get_profile_picture(request.user)}))
    return HttpResponse("NO :(")


def get_responses(request, post):
    posts = Post.objects.filter(main_post=get_object_or_404(Post, id=post)).select_related().order_by('-date')
    posts_dict = [
        {"id": x.id, "content": x.content, "author": x.author.user.get_full_name(), "login": x.author.user.username,
         "picture_url": get_profile_picture(x.author),
         "thumb_ups": [len(Reaction.objects.filter(post=x, value=Thumb.UP)),
                       reaction_exist_value(x, request.user, Thumb.UP)],
         "thumb_downs": [len(Reaction.objects.filter(post=x, value=Thumb.DOWN)),
                         reaction_exist_value(x, request.user, Thumb.DOWN)]}
        for x
        in posts]
    return HttpResponse(dumps(posts_dict))


@login_required
def change_visibility(request):
    if request.POST:
        form = VisibilityForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=form.cleaned_data["post"])
            if post.author != get_profile_by_user(request.user):
                return HttpResponse("0")
            post.visibility = form.cleaned_data["visibility"]
            post.save()
            return HttpResponse("1")
    return HttpResponse("0")


@login_required
def settings(request):
    picture_url = get_profile_by_user(request.user).picture_url
    if picture_url is None:
        picture_url = ""
    ctx = {
        "name_form": ChangeName(initial={'new_name': request.user.first_name, 'new_surname': request.user.last_name,
                                         'new_picture_url': picture_url}),
        "pass_form": ChangePassword,
        "logged_user": get_object_or_404(Profile, user=request.user)
    }
    return render(request, 'website/settings.html', ctx)


@login_required
def change_name(request):
    if request.POST:
        form = ChangeName(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["new_name"]
            request.user.last_name = form.cleaned_data["new_surname"]
            profile = get_profile_by_user(request.user)
            profile.picture_url = form.cleaned_data["new_picture_url"]
            request.user.save()
            profile.save()
    return redirect("/profile/" + request.user.username)


@login_required
def change_password(request):
    if request.POST:
        form = ChangePassword(request.POST)
        if form.is_valid() and request.user.check_password(form.cleaned_data["old_password"]):
            if form.cleaned_data["new_password"] == form.cleaned_data["new_password_repeat"]:
                request.user.set_password(form.cleaned_data["new_password"])
                request.user.save()
            return redirect("/settings/")

    return redirect("/profile/" + request.user.username)
