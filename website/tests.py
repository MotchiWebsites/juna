import re

from django.test import TestCase, override_settings
from django.urls import reverse

from website.navigation import PRIMARY_NAVIGATION
from website.templatetags.navigation_tags import FAVICON_PATHS


class HomepageTests(TestCase):
    def test_homepage_renders_with_combined_metadata(self):
        url = reverse("website:home")
        response = self.client.get(url)

        self.assertEqual(url, "/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "<title>Juna | Creative Team</title>",
            html=True,
        )
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="keywords"')
        self.assertContains(response, "Juna portfolio")
        self.assertContains(response, "independent creative studio")
        self.assertContains(response, "brand strategy")
        self.assertContains(response, "design project inquiry")
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'property="og:description"')
        self.assertContains(
            response,
            '<main id="site-content" tabindex="-1">',
        )

    def test_removed_standalone_page_routes_return_not_found(self):
        for path in ("/work/", "/about/", "/services/", "/contact/"):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 404)

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

    def test_homepage_sections_use_progressive_scroll_reveals(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, "data-reveal", count=5)
        self.assertContains(
            response,
            'src="/static/js/scroll-reveal.js"',
        )

    def test_all_images_include_intrinsic_dimensions(self):
        response = self.client.get(reverse("website:home"))
        image_tags = re.findall(r"<img\b[^>]*>", response.content.decode())

        self.assertTrue(image_tags)
        for image_tag in image_tags:
            with self.subTest(image=image_tag):
                self.assertRegex(image_tag, r'\bwidth="\d+"')
                self.assertRegex(image_tag, r'\bheight="\d+"')

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
        response = self.client.get(f"{reverse('website:home')}?ref=test")

        self.assertContains(
            response,
            '<link rel="canonical" href="https://juna.example/">',
            html=True,
        )
        self.assertContains(
            response,
            'content="https://juna.example/"',
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
