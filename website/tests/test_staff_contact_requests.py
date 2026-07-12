from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from website.models import ContactSubmission


class StaffContactRequestTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.admin = user_model.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        cls.submission = ContactSubmission.objects.create(
            name="Jordan Lee",
            organization="Conscious Studio",
            email="jordan@example.com",
            description=(
                "We need a complete visual identity and a thoughtful website."
            ),
        )
        ContactSubmission.objects.create(
            name="Taylor Morgan",
            organization="",
            email="taylor@example.com",
            description="We would like help with an email campaign.",
            status=ContactSubmission.Status.RESOLVED,
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_anonymous_users_are_sent_to_admin_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("website_staff:contact_request_list")
        )

        self.assertRedirects(
            response,
            (
                f"{reverse('admin:login')}?next="
                f"{reverse('website_staff:contact_request_list')}"
            ),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            response.headers["X-Robots-Tag"],
            "noindex, nofollow",
        )
        self.assertEqual(response.headers["Cache-Control"], "private, no-store")

    def test_staff_without_model_permission_receives_forbidden(self):
        restricted_staff = get_user_model().objects.create_user(
            username="restricted",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(restricted_staff)

        response = self.client.get(
            reverse("website_staff:contact_request_list")
        )

        self.assertEqual(response.status_code, 403)

    def test_view_only_staff_cannot_update_status(self):
        viewer = get_user_model().objects.create_user(
            username="viewer",
            password="test-password",
            is_staff=True,
        )
        viewer.user_permissions.add(
            Permission.objects.get(codename="view_contactsubmission")
        )
        self.client.force_login(viewer)

        detail_response = self.client.get(
            reverse(
                "website_staff:contact_request_detail",
                args=(self.submission.pk,),
            )
        )
        update_response = self.client.post(
            reverse(
                "website_staff:update_contact_request_status",
                args=(self.submission.pk,),
            ),
            {"status": ContactSubmission.Status.RESOLVED},
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(
            detail_response,
            "permission to view this request but not to change",
        )
        self.assertNotContains(detail_response, "Save status")
        self.assertEqual(update_response.status_code, 403)
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, ContactSubmission.Status.NEW)

    def test_custom_admin_login_uses_juna_design(self):
        self.client.logout()

        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back")
        self.assertContains(response, "Sign in with your Juna staff account")
        self.assertContains(response, 'autocomplete="username"')
        self.assertContains(response, 'autocomplete="current-password"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, "Juna Staff Login")
        self.assertContains(response, "Main website", count=2)
        self.assertContains(response, "data-admin-login-form")
        self.assertContains(response, "data-password-input")
        self.assertContains(response, "data-password-toggle")
        self.assertContains(response, 'src="/static/js/admin-auth.js"')
        self.assertContains(response, 'src="/static/js/toasts.js"')
        self.assertEqual(
            response.headers["X-Robots-Tag"],
            "noindex, nofollow",
        )

    def test_invalid_admin_login_uses_error_toast(self):
        self.client.logout()

        response = self.client.post(
            reverse("admin:login"),
            {"username": "admin", "password": "incorrect-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unable to Sign In")
        self.assertContains(response, "data-toast")
        self.assertContains(response, 'role="alert"')

    def test_admin_login_handles_vercel_rate_limits_in_place(self):
        script = (
            Path(__file__).resolve().parents[2] / "static/js/admin-auth.js"
        ).read_text()

        self.assertIn("response.status === 429", script)
        self.assertIn("Too Many Attempts", script)
        self.assertIn("Try again in 10 minutes", script)

    def test_admin_logout_uses_juna_design_and_main_site_link(self):
        response = self.client.post(reverse("admin:logout"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signed Out")
        self.assertContains(response, "You have been signed out securely")
        self.assertContains(response, "View Main Website")
        self.assertContains(response, reverse("admin:login"))

    def test_admin_console_has_title_case_and_main_site_access(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff Administration")
        self.assertContains(response, "Juna Administration")
        self.assertContains(response, "View Main Website")
        self.assertContains(response, 'src="/static/images/juna_logo.png"')
        self.assertContains(response, 'src="/static/js/admin-messages.js"')

    def test_staff_workspace_supports_head_requests(self):
        response = self.client.head(
            reverse("website_staff:contact_request_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertEqual(response.headers["Cache-Control"], "private, no-store")

    def test_short_staff_url_redirects_to_workspace(self):
        response = self.client.get(reverse("website:staff_portal"))

        self.assertRedirects(
            response,
            reverse("website_staff:contact_request_list"),
            fetch_redirect_response=False,
        )

    def test_public_site_shows_portal_link_only_to_authorized_staff(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(
            response,
            f'href="{reverse("website:staff_portal")}"',
            count=2,
        )

        self.client.logout()
        response = self.client.get(reverse("website:home"))
        self.assertNotContains(
            response,
            f'href="{reverse("website:staff_portal")}"',
        )

    def test_list_shows_summary_and_responsive_request_views(self):
        response = self.client.get(
            reverse("website_staff:contact_request_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact requests")
        self.assertContains(response, "Jordan Lee")
        self.assertContains(response, "Taylor Morgan")
        self.assertContains(
            response,
            '<meta name="robots" content="noindex,nofollow" />',
            html=True,
        )
        self.assertContains(response, "data-toast", count=0)
        self.assertContains(response, 'id="request-list"')
        self.assertNotContains(response, 'id="request-detail-panel"')
        self.assertContains(response, "md:hidden")
        self.assertContains(response, "md:block")
        self.assertContains(response, 'name="presentation"', count=4)
        self.assertContains(response, 'hx-trigger="change"', count=4)
        self.assertContains(response, "data-status-select", count=4)
        self.assertContains(response, 'src="/static/js/admin-ui.js"')

    def test_search_and_status_filters_limit_results(self):
        response = self.client.get(
            reverse("website_staff:contact_request_list"),
            {
                "q": "Taylor",
                "status": ContactSubmission.Status.RESOLVED,
            },
        )

        self.assertContains(response, "Taylor Morgan")
        self.assertNotContains(response, "Jordan Lee")

    def test_empty_filters_render_an_empty_state(self):
        response = self.client.get(
            reverse("website_staff:contact_request_list"),
            {"q": "No matching request"},
        )

        self.assertContains(
            response,
            "No requests match these filters.",
            count=2,
        )

    def test_detail_uses_a_complete_bookmarkable_page(self):
        response = self.client.get(
            reverse(
                "website_staff:contact_request_detail",
                args=(self.submission.pk,),
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jordan Lee")
        self.assertContains(response, self.submission.description)
        self.assertContains(response, "Update status")
        self.assertContains(response, "<h1")
        self.assertContains(response, "<html")
        self.assertContains(response, "Back to contact requests")
        self.assertContains(response, "data-status-select")
        self.assertNotRegex(
            response.content.decode(),
            r'whitespace-pre-line[^>]*>\s+We need a complete visual identity',
        )

    def test_htmx_status_update_refreshes_detail_list_and_toast(self):
        response = self.client.post(
            reverse(
                "website_staff:update_contact_request_status",
                args=(self.submission.pk,),
            ),
            {
                "status": ContactSubmission.Status.IN_PROGRESS,
                "presentation": "inline",
                "control_id": "table",
            },
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.submission.refresh_from_db()
        self.assertEqual(
            self.submission.status,
            ContactSubmission.Status.IN_PROGRESS,
        )
        self.assertEqual(response.headers["HX-Trigger"], "contactStatusChanged")
        self.assertContains(response, "In Progress")
        self.assertContains(response, "data-status-control")
        self.assertContains(response, f'id="status-table-{self.submission.pk}"')
        self.assertContains(response, 'hx-swap-oob="beforeend:#toast-region"')
        self.assertContains(response, "was updated")

    def test_non_htmx_status_update_redirects_to_detail(self):
        response = self.client.post(
            reverse(
                "website_staff:update_contact_request_status",
                args=(self.submission.pk,),
            ),
            {"status": ContactSubmission.Status.RESOLVED},
        )

        self.assertRedirects(
            response,
            reverse(
                "website_staff:contact_request_detail",
                args=(self.submission.pk,),
            ),
            fetch_redirect_response=False,
        )

    def test_django_admin_model_link_opens_staff_workspace(self):
        response = self.client.get(
            reverse("admin:website_contactsubmission_changelist")
        )

        self.assertRedirects(
            response,
            reverse("website_staff:contact_request_list"),
            fetch_redirect_response=False,
        )
