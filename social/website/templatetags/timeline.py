import logging
import re
from html import escape
from django import template

from website.libs.model_utils import is_user_followed_by, get_profile_by_user

register = template.Library()

get_tags = lambda post: re.findall(r"#(\w+)", post)
split = lambda post: re.split(r"#\w+", post)

@register.filter(name="add_tags")
def post_with_tags(post):
    post_list = []
    tags = get_tags(post)
    not_tags = list(map(lambda part: escape(part), split(post)))
    for i, tag in enumerate(tags):
        post_list.append(not_tags[i])
        post_list.append('<a href="/tag/{}">'.format(tag) + '#' + tag + '</a>')
    post_list.append(not_tags[-1])
    return "".join(post_list)


@register.filter(name="thumb_value")
def get_thumb_value(value, user):
    user = get_profile_by_user(user)
    return value.get_thumb_value(user.user)


@register.filter(name="followed_by")
def is_followed_by(user1, user2):
    return is_user_followed_by(user1, user2)
