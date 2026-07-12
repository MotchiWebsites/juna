"""Settings that keep automated tests isolated from external services."""

from .settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# The test client is intentionally in-process and does not traverse Vercel's
# HTTPS edge. Production redirect behavior is covered by Django's deploy check.
SECURE_SSL_REDIRECT = False

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
