from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.urls import include, path, re_path

urlpatterns = [
    path(
        "admin-portal/contact-requests/",
        include("website.staff_urls"),
    ),
    path("admin-portal/", admin.site.urls),
    path("", include("website.urls")),
]

if settings.DEBUG:
    urlpatterns.insert(
        0,
        re_path(r"^static/(?P<path>.*)$", serve_static),
    )
