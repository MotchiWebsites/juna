from pathlib import Path
import os
from urllib.parse import parse_qsl, unquote, urlparse

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.utils.csp import CSP

BASE_DIR = Path(__file__).resolve().parent.parent

# Local development only; production should provide environment variables directly.
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "t")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# Trust exact Vercel deployment aliases when system variables are exposed.
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
        ALLOWED_HOSTS.extend(sorted(vercel_hosts))
        CSRF_TRUSTED_ORIGINS.extend(
            f"https://{host}" for host in sorted(vercel_hosts)
        )
    else:
        # Preserve preview support when system variables are disabled.
        ALLOWED_HOSTS.append(".vercel.app")
        CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")

# Public origin used for canonical and social-sharing URLs.
# Leave it empty locally to use the current request origin.
SITE_URL = os.getenv("SITE_URL", "").strip().rstrip("/")
if not DEBUG:
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

# Preview URLs should be testable but must never compete with production search.
IS_VERCEL_PREVIEW = os.getenv("VERCEL_ENV") == "preview"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "website.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csp",
                "website.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

database_url = os.getenv("DATABASE_URL", "").strip()

if database_url:
    parsed_database_url = urlparse(database_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote(parsed_database_url.path.lstrip("/")),
            "USER": unquote(parsed_database_url.username or ""),
            "PASSWORD": unquote(parsed_database_url.password or ""),
            "HOST": parsed_database_url.hostname or "",
            "PORT": parsed_database_url.port or 5432,
            "OPTIONS": dict(parse_qsl(parsed_database_url.query)),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "America/Toronto")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Keep browser capabilities and resource origins explicit. JSON-LD receives a
# per-request nonce in the homepage template; executable scripts are local.
SECURE_CSP = {
    "default-src": [CSP.SELF],
    "base-uri": [CSP.SELF],
    "connect-src": [CSP.SELF],
    "font-src": [CSP.SELF, "https://use.typekit.net"],
    "form-action": [CSP.SELF],
    "frame-ancestors": [CSP.NONE],
    "img-src": [CSP.SELF, "data:"],
    "manifest-src": [CSP.SELF],
    "object-src": [CSP.NONE],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [
        CSP.SELF,
        "https://use.typekit.net",
        "https://p.typekit.net",
    ],
}

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Vercel captures stdout/stderr from Functions. Avoid logging request bodies or
# form data because contact submissions contain personal information.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "server": {
            "format": "{levelname} {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "server",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO").upper(),
            "propagate": False,
        },
    },
}

# Vercel terminates HTTPS before forwarding requests to Django.
if os.getenv("VERCEL"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(
        os.getenv("DJANGO_SECURE_HSTS_SECONDS", "3600")
    )
    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        os.getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower()
        in ("true", "1", "t")
    )
    SECURE_HSTS_PRELOAD = (
        os.getenv("DJANGO_SECURE_HSTS_PRELOAD", "False").lower()
        in ("true", "1", "t")
    )
