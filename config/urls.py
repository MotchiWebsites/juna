from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin-portal/contact-requests/",
        include("website.staff_urls"),
    ),
    path("admin-portal/", admin.site.urls),
    path("", include("website.urls")),
]
