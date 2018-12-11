import logging

from django import template

from website.lib.model_utils import is_user_followed_by

register = template.Library()


@register.filter(name="thumb_value")
def get_thumb_value(value, user):
    return value.get_thumb_value(user)
    pass


@register.filter(name="followed_by")
def is_followed_by(user1, user2):
    return is_user_followed_by(user1, user2)
    pass
