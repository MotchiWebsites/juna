from django.contrib import admin
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

    def test_organization_is_optional(self):
        form = ContactForm(
            {
                "name": "A prospective client",
                "organization": "",
                "email": "client@example.com",
                "description": "A thoughtful project description.",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)


class ContactSectionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {
            "name": "A prospective client",
            "organization": "Example Studio",
            "email": "client@example.com",
            "description": "A thoughtful project description.",
        }

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
        self.assertContains(
            response,
            f'action="{reverse("website:submit_contact")}"',
        )
        self.assertContains(
            response,
            f'hx-post="{reverse("website:submit_contact")}"',
        )
        self.assertContains(response, 'hx-target="#contact-form"')
        self.assertContains(response, 'hx-swap="outerHTML"')
        self.assertContains(response, 'id="toast-region"')
        self.assertContains(response, 'src="/static/js/toasts.js"')

    def test_form_preserves_values_and_renders_validation_errors(self):
        response = self.client.post(
            reverse("website:submit_contact"),
            {
                "name": "A prospective client",
                "organization": "Example Studio",
                "email": "not-an-email",
                "description": "",
            },
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertContains(response, 'value="A prospective client"')
        self.assertContains(response, 'value="Example Studio"')
        self.assertContains(response, 'aria-invalid="true"', count=2)
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "This field is required.")
        self.assertNotContains(response, "<html")

    def test_valid_htmx_submission_saves_and_returns_toast(self):
        response = self.client.post(
            reverse("website:submit_contact"),
            self.valid_data,
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        submission = ContactSubmission.objects.get()
        self.assertEqual(submission.name, self.valid_data["name"])
        self.assertEqual(
            submission.organization,
            self.valid_data["organization"],
        )
        self.assertEqual(submission.email, self.valid_data["email"])
        self.assertEqual(
            submission.status,
            ContactSubmission.Status.NEW,
        )
        self.assertContains(response, 'id="contact-form"')
        self.assertContains(response, 'hx-swap-oob="beforeend:#toast-region"')
        self.assertContains(
            response,
            "Thanks! We received your project details.",
        )
        self.assertNotContains(
            response,
            'value="A prospective client"',
        )

    def test_valid_non_htmx_submission_uses_post_redirect_get(self):
        response = self.client.post(
            reverse("website:submit_contact"),
            self.valid_data,
            follow=True,
        )

        self.assertRedirects(response, f'{reverse("website:home")}#contact')
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertContains(
            response,
            "Thanks! We received your project details.",
        )

    def test_invalid_non_htmx_submission_renders_full_page(self):
        invalid_data = {
            **self.valid_data,
            "email": "not-an-email",
        }

        response = self.client.post(
            reverse("website:submit_contact"),
            invalid_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertContains(response, "<html")
        self.assertContains(response, 'value="A prospective client"')
        self.assertContains(response, "Enter a valid email address.")

    def test_submission_endpoint_rejects_get_requests(self):
        response = self.client.get(reverse("website:submit_contact"))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.headers["X-Robots-Tag"],
            "noindex, nofollow",
        )
        self.assertEqual(response.headers["Cache-Control"], "private, no-store")


class ContactSubmissionAdminTests(TestCase):
    def test_model_is_registered_with_admin(self):
        self.assertTrue(admin.site.is_registered(ContactSubmission))
