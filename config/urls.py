from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin-portal/", admin.site.urls),
    path("", include("website.urls")),
]
