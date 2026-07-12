"""Settings for local development and Django's HTTP runserver."""

from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

# Load local variables before base settings build DATABASES and shared defaults.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .base_settings import *  # noqa: F403
from .base_settings import _env_csv  # noqa: F401

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("true", "1", "t")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "").strip() or SECRET_KEY
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    *_env_csv("DJANGO_ALLOWED_HOSTS"),
]
CSRF_TRUSTED_ORIGINS = _env_csv("DJANGO_CSRF_TRUSTED_ORIGINS")

raw_site_url = os.getenv("SITE_URL", "").strip().rstrip("/")
if not raw_site_url:
    SITE_URL = "http://127.0.0.1:8000"
else:
    parsed_site_url = urlparse(raw_site_url)
    if parsed_site_url.hostname == "localhost":
        SITE_URL = raw_site_url.replace("localhost", "127.0.0.1")
    else:
        SITE_URL = raw_site_url

local_csrf_origin = "http://127.0.0.1:8000"
CSRF_TRUSTED_ORIGINS = [
    origin.replace("localhost", "127.0.0.1") for origin in CSRF_TRUSTED_ORIGINS
]
if local_csrf_origin not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(local_csrf_origin)
IS_VERCEL_PREVIEW = False

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
