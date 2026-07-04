from django.contrib import admin
from django.shortcuts import redirect

from .models import ContactSubmission

admin.site.site_header = "Juna administration"
admin.site.site_title = "Juna admin"
admin.site.index_title = "Staff administration"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "email",
        "status",
        "submitted_at",
    )
    list_filter = ("status", "submitted_at")
    search_fields = ("name", "organization", "email")
    readonly_fields = (
        "name",
        "organization",
        "email",
        "description",
        "submitted_at",
    )
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
    list_per_page = 50

    def changelist_view(self, request, extra_context=None):
        return redirect("website_staff:contact_request_list")
