from django.contrib import admin
from django.urls import path

from . import staff_views, views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path(
        "staff/",
        admin.site.admin_view(staff_views.staff_portal),
        name="staff_portal",
    ),
    path("contact/submit/", views.submit_contact, name="submit_contact"),
]
