from django import template

from website.content.navigation import PRIMARY_NAVIGATION

register = template.Library()

@register.inclusion_tag(
    "website/partials/components/navigation/navigation_links.html",
)
def primary_navigation():
    return {
        "navigation_items": PRIMARY_NAVIGATION,
    }
