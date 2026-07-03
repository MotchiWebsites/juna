from django.test import TestCase
from django.urls import reverse

from website.forms import ContactForm
from website.models import ContactSubmission


class ContactFormTests(TestCase):
    def test_form_uses_contact_submission_model(self):
        self.assertIs(ContactForm._meta.model, ContactSubmission)
        self.assertEqual(
            ContactForm._meta.fields,
            ("name", "organization", "email", "description"),
        )


class ContactSectionTests(TestCase):
    def test_section_renders_accessible_unbound_form(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, 'aria-labelledby="contact-title"')
        self.assertContains(response, "Tell us about your project")
        self.assertContains(response, "data-contact-form", count=1)
        self.assertContains(response, 'type="email"', count=1)
        self.assertContains(response, 'autocomplete="name"', count=1)
        self.assertContains(response, 'autocomplete="organization"', count=1)
        self.assertContains(response, 'autocomplete="email"', count=1)
        self.assertContains(response, 'name="csrfmiddlewaretoken"', count=1)
        self.assertContains(response, "<textarea", count=1)
        self.assertContains(response, "Start chatting")

    def test_form_preserves_values_and_renders_validation_errors(self):
        response = self.client.post(
            reverse("website:home"),
            {
                "name": "A prospective client",
                "organization": "Example Studio",
                "email": "not-an-email",
                "description": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="A prospective client"')
        self.assertContains(response, 'value="Example Studio"')
        self.assertContains(response, 'aria-invalid="true"', count=2)
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "This field is required.")
