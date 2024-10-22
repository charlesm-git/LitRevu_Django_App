from django import template

register = template.Library()


@register.filter
def stars(rating):
    filled_stars = "★" * rating
    empty_stars = "☆" * (5 - rating)
    return filled_stars + empty_stars


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag
def display_username(post_user, logged_in_user):
    if post_user == logged_in_user:
        return "vous"
    else:
        return post_user.username
