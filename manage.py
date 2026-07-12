#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def get_default_settings_module(argv):
    if len(argv) > 1 and argv[1] == "test":
        return "config.test_settings"

    if len(argv) > 1 and argv[1] == "runserver":
        return "config.local_settings"

    return "config.local_settings"


def main():
    """Run administrative tasks."""
    default_settings = get_default_settings_module(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] in {"runserver", "test"}:
        os.environ["DJANGO_SETTINGS_MODULE"] = default_settings
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
