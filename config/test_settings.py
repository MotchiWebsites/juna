"""Settings that keep automated tests isolated from external services."""

from .base_settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1", "[::1]"]
CSRF_TRUSTED_ORIGINS = []
SITE_URL = ""
DEBUG = False

# The test client is intentionally in-process and does not traverse Vercel's
# HTTPS edge. Production redirect behavior is covered by Django's deploy check.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
