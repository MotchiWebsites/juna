from django import forms

from ..models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Collect and validate a prospective client's project details."""

    class Meta:
        model = ContactSubmission
        fields = ("name", "organization", "email", "description")
        labels = {
            "name": "Name",
            "organization": "Organization (optional)",
            "email": "Email",
            "description": "Project description",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "name",
                    "placeholder": "Name",
                }
            ),
            "organization": forms.TextInput(
                attrs={
                    "autocomplete": "organization",
                    "placeholder": "Organization (optional)",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "placeholder": "Email",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Tell us a little about your project",
                    "rows": 8,
                }
            ),
        }


class ContactSubmissionStatusForm(forms.ModelForm):
    """Allow staff to update only a submission's workflow status."""

    class Meta:
        model = ContactSubmission
        fields = ("status",)
