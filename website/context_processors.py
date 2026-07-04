from django.conf import settings


def get_site_url(request):
    site_url = settings.SITE_URL.rstrip("/")
    if not site_url:
        site_url = request.build_absolute_uri("/").rstrip("/")

    return site_url


def site_settings(request):
    site_url = get_site_url(request)

    return {
        "canonical_url": f"{site_url}{request.path}",
        "site_url": site_url,
    }
