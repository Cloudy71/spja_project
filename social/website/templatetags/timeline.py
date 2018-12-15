import logging

from django import template

from website.libs.model_utils import is_user_followed_by, get_profile_by_user

register = template.Library()


@register.filter(name="thumb_value")
def get_thumb_value(value, user):
    user = get_profile_by_user(user)
    return value.get_thumb_value(user.user)
    pass


@register.filter(name="followed_by")
def is_followed_by(user1, user2):
    return is_user_followed_by(user1, user2)
    pass
