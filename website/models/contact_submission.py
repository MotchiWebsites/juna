from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactSubmission(models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("New")
        IN_PROGRESS = "in_progress", _("In Progress")
        RESOLVED = "resolved", _("Resolved")
        ARCHIVED = "archived", _("Archived")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    organization = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Organization"),
    )
    email = models.EmailField(verbose_name=_("Email"))
    description = models.TextField(max_length=2000, verbose_name=_("Description"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_submissions"
        ordering = ("-submitted_at",)
        verbose_name = _("Contact submission")
        verbose_name_plural = _("Contact submissions")

    def __str__(self) -> str:
        return f"{self.name} — {self.email}"
