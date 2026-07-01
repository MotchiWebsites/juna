from secrets import choice

from django import template

from website.navigation import PRIMARY_NAVIGATION

register = template.Library()

FAVICON_PATHS = tuple(
    f"icons/{color}_{shape}.svg"
    for color in ("blue", "green", "pink", "yellow")
    for shape in ("circle", "square", "star", "triangle")
)


@register.inclusion_tag(
    "website/partials/navigation_links.html",
)
def primary_navigation():
    return {
        "navigation_items": PRIMARY_NAVIGATION,
    }


@register.simple_tag
def random_favicon():
    return choice(FAVICON_PATHS)
