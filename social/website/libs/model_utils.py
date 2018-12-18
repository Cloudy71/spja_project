from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_profile_by_user(user):
    from website.models import Profile
    if isinstance(user, Profile):
        return user
    try:
        return Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


def is_user_followed_by(user, follower):
    from website.models import Follow
    user = get_profile_by_user(user)
    follower = get_profile_by_user(follower)
    try:
        Follow.objects.get(follower=follower, following=user)
        return True
    except ObjectDoesNotExist:
        return False
    pass


def post_exists(post_id):
    from website.models import Post
    try:
        Post.objects.get(id=post_id)
        return True
    except ObjectDoesNotExist:
        return False


def profile_exists_by_username(username):
    from website.models import Profile
    try:
        user = User.objects.get(username=username)
        Profile.objects.get(user=user)
        return True
    except ObjectDoesNotExist:
        return False


def reaction_exist(post, user):
    user = get_profile_by_user(user)
    try:
        from website.models import Reaction
        Reaction.objects.get(author=user, post=post)
        return True
    except ObjectDoesNotExist:
        return False


def reaction_exist_value(post, user, value):
    user = get_profile_by_user(user)
    try:
        from website.models import Reaction
        Reaction.objects.get(author=user, post=post, value=value)
        return True
    except ObjectDoesNotExist:
        return False


def follow_exist(follower, following):
    follower = get_profile_by_user(follower)
    following = get_profile_by_user(following)
    try:
        from website.models import Follow
        Follow.objects.get(following=following, follower=follower)
        return True
    except ObjectDoesNotExist:
        return False
