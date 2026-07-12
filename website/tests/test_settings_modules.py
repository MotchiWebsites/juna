import importlib
import os
import sys
from io import StringIO
from unittest import mock

from django.test import SimpleTestCase


def load_settings_module(module_name, environment):
    with mock.patch.dict(os.environ, environment, clear=False):
        for loaded_module_name in (
            "config.base_settings",
            "config.local_settings",
            "config.production_settings",
        ):
            sys.modules.pop(loaded_module_name, None)
        return importlib.import_module(module_name)


class SettingsModuleTests(SimpleTestCase):
    def test_manage_defaults_to_local_settings_for_runserver(self):
        manage = importlib.import_module("manage")

        self.assertEqual(
            manage.get_default_settings_module(["manage.py", "runserver"]),
            "config.local_settings",
        )
        self.assertEqual(
            manage.get_default_settings_module(["manage.py", "test"]),
            "config.test_settings",
        )
        self.assertEqual(
            manage.get_default_settings_module(["manage.py", "check"]),
            "config.local_settings",
        )

    def test_manage_overrides_settings_module_for_runserver(self):
        manage = importlib.import_module("manage")

        with mock.patch.dict(
            os.environ,
            {"DJANGO_SETTINGS_MODULE": "config.production_settings"},
            clear=False,
        ):
            with mock.patch(
                "django.core.management.execute_from_command_line",
                side_effect=SystemExit,
            ):
                with mock.patch.object(sys, "argv", ["manage.py", "runserver"]):
                    with self.assertRaises(SystemExit):
                        manage.main()

            self.assertEqual(
                os.environ["DJANGO_SETTINGS_MODULE"],
                "config.local_settings",
            )

    def test_manage_preserves_explicit_settings_for_non_local_commands(self):
        manage = importlib.import_module("manage")

        with mock.patch.dict(
            os.environ,
            {"DJANGO_SETTINGS_MODULE": "config.production_settings"},
            clear=False,
        ):
            with mock.patch("sys.stdout", new=StringIO()):
                with mock.patch.object(sys, "argv", ["manage.py", "help"]):
                    manage.main()

            self.assertEqual(
                os.environ["DJANGO_SETTINGS_MODULE"],
                "config.production_settings",
            )

    def test_local_settings_keep_http_redirects_disabled(self):
        local_settings = load_settings_module(
            "config.local_settings",
            {
                "DJANGO_SECRET_KEY": "local-test-secret",
                "SITE_URL": "http://localhost:8000",
                "DJANGO_CSRF_TRUSTED_ORIGINS": "http://localhost:8000",
                "DJANGO_DEBUG": "True",
            },
        )

        self.assertFalse(local_settings.SECURE_SSL_REDIRECT)
        self.assertFalse(local_settings.SESSION_COOKIE_SECURE)
        self.assertFalse(local_settings.CSRF_COOKIE_SECURE)
        self.assertEqual(local_settings.SITE_URL, "http://127.0.0.1:8000")
        self.assertEqual(
            local_settings.CSRF_TRUSTED_ORIGINS,
            ["http://127.0.0.1:8000"],
        )

    def test_local_settings_load_env_before_database_defaults(self):
        local_settings = load_settings_module(
            "config.local_settings",
            {
                "DJANGO_SECRET_KEY": "local-test-secret",
                "DATABASE_URL": "postgres://juna:secret@db.example:5432/juna",
                "DJANGO_DEBUG": "True",
            },
        )

        self.assertEqual(
            local_settings.DATABASES["default"]["ENGINE"],
            "django.db.backends.postgresql",
        )
        self.assertEqual(local_settings.DATABASES["default"]["NAME"], "juna")
        self.assertEqual(local_settings.DATABASES["default"]["HOST"], "db.example")

    def test_local_settings_do_not_use_blank_secret_key(self):
        local_settings = load_settings_module(
            "config.local_settings",
            {
                "DJANGO_SECRET_KEY": "",
                "DJANGO_DEBUG": "True",
            },
        )

        self.assertTrue(local_settings.SECRET_KEY)

    def test_production_settings_enforce_https_security_defaults(self):
        production_settings = load_settings_module(
            "config.production_settings",
            {
                "DJANGO_SECRET_KEY": "production-test-secret",
                "SITE_URL": "https://juna.example",
                "DJANGO_ALLOWED_HOSTS": "juna.example",
                "DJANGO_CSRF_TRUSTED_ORIGINS": "https://juna.example",
            },
        )

        self.assertTrue(production_settings.SECURE_SSL_REDIRECT)
        self.assertTrue(production_settings.SESSION_COOKIE_SECURE)
        self.assertTrue(production_settings.CSRF_COOKIE_SECURE)
        self.assertEqual(production_settings.SECURE_HSTS_SECONDS, 31536000)
        self.assertTrue(production_settings.SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertTrue(production_settings.SECURE_HSTS_PRELOAD)
        self.assertIn("juna.example", production_settings.ALLOWED_HOSTS)
        self.assertIn("https://juna.example", production_settings.CSRF_TRUSTED_ORIGINS)

    def test_production_settings_reject_blank_secret_key(self):
        from django.core.exceptions import ImproperlyConfigured

        with self.assertRaisesRegex(ImproperlyConfigured, "DJANGO_SECRET_KEY"):
            load_settings_module(
                "config.production_settings",
                {
                    "DJANGO_SECRET_KEY": "",
                    "SITE_URL": "https://juna.example",
                },
            )
