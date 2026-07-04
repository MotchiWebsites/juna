from django.contrib import admin
from django.urls import path

from . import staff_views

app_name = "website_staff"

urlpatterns = [
    path(
        "",
        admin.site.admin_view(staff_views.contact_request_list),
        name="contact_request_list",
    ),
    path(
        "<int:submission_id>/",
        admin.site.admin_view(staff_views.contact_request_detail),
        name="contact_request_detail",
    ),
    path(
        "<int:submission_id>/status/",
        admin.site.admin_view(staff_views.update_contact_request_status),
        name="update_contact_request_status",
    ),
]
