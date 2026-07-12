"""Compatibility shim for older imports.

Prefer importing config.local_settings or config.production_settings directly.
"""

import os
from urllib.parse import parse_qsl, unquote, urlparse

_use_local_settings = os.getenv("DJANGO_DEBUG", "True").lower() in (
    "true",
    "1",
    "t",
)

if _use_local_settings:
    from .local_settings import *  # noqa: F403
else:
    from .production_settings import *  # noqa: F403
