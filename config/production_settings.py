"""Settings for production deployments."""

from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from .base_settings import *  # noqa: F403
from .base_settings import _env_bool, _env_csv  # noqa: F401

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")
DEBUG = False

SITE_URL = os.getenv("SITE_URL", "").strip().rstrip("/")
parsed_site_url = urlparse(SITE_URL)
if (
    parsed_site_url.scheme != "https"
    or not parsed_site_url.netloc
    or parsed_site_url.path
    or parsed_site_url.params
    or parsed_site_url.query
    or parsed_site_url.fragment
):
    raise ImproperlyConfigured(
        "SITE_URL must be a path-free HTTPS origin in production."
    )

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

if parsed_site_url.netloc:
    ALLOWED_HOSTS.append(parsed_site_url.netloc)
    CSRF_TRUSTED_ORIGINS.append(f"https://{parsed_site_url.netloc}")

for host in _env_csv("DJANGO_ALLOWED_HOSTS"):
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

for origin in _env_csv("DJANGO_CSRF_TRUSTED_ORIGINS"):
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

if os.getenv("VERCEL"):
    vercel_hosts = {
        os.getenv(variable, "").strip()
        for variable in (
            "VERCEL_URL",
            "VERCEL_BRANCH_URL",
            "VERCEL_PROJECT_PRODUCTION_URL",
        )
    } - {""}
    if vercel_hosts:
        for host in sorted(vercel_hosts):
            if host not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(host)
            origin = f"https://{host}"
            if origin not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(origin)
    else:
        if ".vercel.app" not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(".vercel.app")
        if "https://*.vercel.app" not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")

IS_VERCEL_PREVIEW = os.getenv("VERCEL_ENV") == "preview"

SECURE_PROXY_SSL_HEADER = (
    ("HTTP_X_FORWARDED_PROTO", "https") if os.getenv("VERCEL") else None
)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "True",
)
SECURE_HSTS_PRELOAD = _env_bool("DJANGO_SECURE_HSTS_PRELOAD", "True")
