from django import forms


class ContactForm(forms.Form):
    """Validate contact details without coupling the UI to persistence."""

    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "placeholder": "Name",
            }
        ),
    )
    organization = forms.CharField(
        label="Organization",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "organization",
                "placeholder": "Organization",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Email",
            }
        ),
    )
    description = forms.CharField(
        label="Project description",
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us a little about your project",
                "rows": 8,
            }
        ),
    )
