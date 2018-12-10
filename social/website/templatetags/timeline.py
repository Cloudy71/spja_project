from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import Follow

register = template.Library()


@register.filter(name="thumb_value")
def get_thumb_value(value, user):
    return value.get_thumb_value(user)
    pass


@register.filter(name="followed_by")
def is_followed_by(user1, user2):
    try:
        Follow.objects.get(follower=user2, following=user1)
        return True
    except ObjectDoesNotExist:
        return False
    pass
