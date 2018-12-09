from django import template

register = template.Library()


@register.filter(name="thumb_value")
def get_thumb_value(value, user):
    return value.get_thumb_value(user)
    pass
