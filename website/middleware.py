from django.conf import settings


PRIVATE_PATH_PREFIXES = ("/admin-portal/", "/staff/", "/contact/submit/")


class SecurityHeadersMiddleware:
    """Add browser restrictions and indexing rules not covered by Django."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers["Permissions-Policy"] = (
            "camera=(), geolocation=(), gyroscope=(), microphone=(), "
            "payment=(), usb=()"
        )

        is_private = request.path.startswith(PRIVATE_PATH_PREFIXES)
        if is_private or settings.IS_VERCEL_PREVIEW:
            response.headers["X-Robots-Tag"] = "noindex, nofollow"

        if is_private:
            response.headers["Cache-Control"] = "private, no-store"

        return response
