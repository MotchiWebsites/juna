import re

from django.test import TestCase, override_settings
from django.urls import reverse

from website.navigation import PRIMARY_NAVIGATION
from website.templatetags.navigation_tags import FAVICON_PATHS


class PublicPageTests(TestCase):
    pages = {
        "home": ("Juna | Creative Team", "/"),
        "work": ("Selected Work | Juna", "/work/"),
        "about": ("About Us | Juna", "/about/"),
        "services": ("Services | Juna", "/services/"),
        "contact": ("Contact | Juna", "/contact/"),
    }

    def test_named_pages_render_with_expected_metadata(self):
        for name, (title, path) in self.pages.items():
            with self.subTest(page=name):
                url = reverse(f"website:{name}")
                response = self.client.get(url)

                self.assertEqual(url, path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f"<title>{title}</title>", html=True)
                self.assertContains(response, 'name="description"')
                self.assertContains(response, 'name="keywords"')
                self.assertContains(response, 'property="og:title"')
                self.assertContains(response, 'property="og:description"')
                self.assertContains(
                    response,
                    '<main id="site-content" tabindex="-1">',
                )

    def test_primary_navigation_targets_homepage_sections(self):
        response = self.client.get(reverse("website:home"))

        for item in PRIMARY_NAVIGATION:
            with self.subTest(section=item.section_id):
                self.assertContains(
                    response,
                    f'href="#{item.section_id}"',
                )
                self.assertContains(
                    response,
                    f'data-section-id="{item.section_id}"',
                    count=2,
                )
                section_matches = re.findall(
                    rf'<section\b[^>]*\bid="{re.escape(item.section_id)}"',
                    response.content.decode(),
                )
                self.assertEqual(len(section_matches), 1)

        for icon in {item.icon for item in PRIMARY_NAVIGATION}:
            expected_count = (
                sum(item.icon == icon for item in PRIMARY_NAVIGATION) * 2
            )
            with self.subTest(icon=icon):
                self.assertContains(
                    response,
                    f'src="/static/{icon}"',
                    count=expected_count,
                )

        self.assertNotContains(response, 'hx-target="#site-content"')
        self.assertNotContains(response, 'hx-push-url="true"')

    def test_overview_is_the_initial_active_section(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, 'aria-current="location"', count=2)

    def test_page_uses_random_favicon_and_stable_touch_icon(self):
        response = self.client.get(reverse("website:home"))
        html = response.content.decode()

        favicon_match = re.search(
            r'rel="icon"[^>]+type="image/svg\+xml"'
            r'[^>]+href="/static/([^"]+)"',
            html,
        )

        self.assertIsNotNone(favicon_match)
        self.assertIn(favicon_match.group(1), FAVICON_PATHS)
        self.assertContains(response, 'rel="apple-touch-icon"')
        self.assertContains(
            response,
            'href="/static/favicon/apple-touch-icon.png"',
        )
        self.assertContains(
            response,
            'href="/static/favicon/favicon.ico"',
        )
        self.assertContains(
            response,
            'href="/static/favicon/favicon-96x96.png"',
        )
        self.assertContains(
            response,
            'href="/static/favicon/site.webmanifest"',
        )

    @override_settings(SITE_URL="https://juna.example/")
    def test_social_metadata_uses_absolute_canonical_urls(self):
        response = self.client.get(f"{reverse('website:about')}?ref=test")

        self.assertContains(
            response,
            '<link rel="canonical" href="https://juna.example/about/">',
            html=True,
        )
        self.assertContains(
            response,
            'content="https://juna.example/about/"',
        )
        self.assertContains(
            response,
            'content="https://juna.example/static/images/social/og-default.png"',
        )
        self.assertContains(
            response,
            'content="https://juna.example/static/images/social/og-twitter.png"',
        )
        self.assertContains(response, 'property="og:image:alt"')
        self.assertContains(response, 'name="twitter:card"')
