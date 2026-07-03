import re

from django.test import TestCase, override_settings
from django.urls import reverse

from website.content.navigation import PRIMARY_NAVIGATION
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

        navigation_links = re.findall(
            r'<a\b(?=[^>]*data-primary-nav-link)[\s\S]*?</a>',
            response.content.decode(),
        )
        self.assertEqual(len(navigation_links), len(PRIMARY_NAVIGATION) * 2)
        for item in PRIMARY_NAVIGATION:
            matching_links = [
                link
                for link in navigation_links
                if f'data-section-id="{item.section_id}"' in link
                and f'src="/static/{item.icon}"' in link
            ]
            with self.subTest(section=item.section_id):
                self.assertEqual(len(matching_links), 2)

        self.assertNotContains(response, 'hx-target="#site-content"')
        self.assertNotContains(response, 'hx-push-url="true"')

    def test_overview_is_the_initial_active_section(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, 'aria-current="location"', count=2)

    def test_overview_has_mobile_scroll_prompt(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, "data-scroll-prompt", count=1)
        self.assertContains(response, 'href="#works"')
        self.assertContains(response, "Scroll to see more")
        self.assertContains(response, "lg:hidden")
        self.assertContains(
            response,
            'src="/static/js/scroll-prompt.js"',
        )

    def test_homepage_sections_use_progressive_scroll_reveals(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, "data-reveal", count=19)
        self.assertContains(response, "data-shared-heading", count=5)
        self.assertContains(
            response,
            'src="/static/js/scroll-reveal.js"',
        )

    def test_homepage_uses_one_h1_and_h2_section_headings(self):
        response = self.client.get(reverse("website:home"))
        html = response.content.decode()

        self.assertEqual(len(re.findall(r"<h1\b", html)), 1)
        self.assertEqual(len(re.findall(r"<h2\b", html)), 4)
        for section_id in ("works", "about", "services", "contact"):
            self.assertRegex(
                html,
                rf'<h2\b[^>]*id="{section_id}-title"',
            )

    def test_about_section_renders_team_profiles_and_static_assets(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, 'aria-labelledby="about-title"')
        self.assertContains(response, "Jun Nguyen")
        self.assertContains(response, "Alicia Symons")
        self.assertContains(response, 'src="/static/images/about/duong.jpg"')
        self.assertContains(response, 'src="/static/images/about/alicia.jpg"')
        self.assertContains(response, "data-team-member", count=2)

    def test_works_section_renders_all_work_items(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, "data-work-item", count=5)
        for image_name in (
            "email-phone.jpg",
            "signage.jpg",
            "lai_project_can.jpg",
            "logo_lai_project.gif",
            "postcard_mockup.jpg",
        ):
            with self.subTest(image=image_name):
                self.assertContains(
                    response,
                    f'src="/static/images/works/{image_name}"',
                )

    def test_services_section_renders_all_services(self):
        response = self.client.get(reverse("website:home"))

        self.assertContains(response, 'aria-labelledby="services-title"')
        self.assertContains(response, "data-service-item", count=6)
        for service_name in (
            "Website",
            "Branding",
            "Advertising",
            "Social Media",
            "Print",
            "Email",
        ):
            with self.subTest(service=service_name):
                self.assertContains(response, service_name)

    def test_contact_section_renders_accessible_unbound_form(self):
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

    def test_contact_form_preserves_values_and_renders_validation_errors(self):
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
            'content="https://juna.example/static/images/social/open-graph/default.png"',
        )
        self.assertContains(
            response,
            'content="https://juna.example/static/images/social/x/home.png"',
        )
        self.assertContains(response, 'property="og:image:alt"')
        self.assertContains(response, 'name="twitter:card"')
