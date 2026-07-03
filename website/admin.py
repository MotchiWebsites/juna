from django.contrib import admin

from .models import ContactSubmission


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
    readonly_fields = ("submitted_at",)
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
    list_per_page = 50
