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
