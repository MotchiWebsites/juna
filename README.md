# Juna

Juna is a Django website for a creative team serving conscious brands. It is a
server-rendered site with a small frontend toolchain for Tailwind CSS and HTMX
assets, and it is configured for deployment on Vercel.

## Tech stack

- Python and Django 6
- Django templates
- Tailwind CSS 4
- HTMX 2
- Vanilla JavaScript with Intersection Observer scroll reveals
- Neon PostgreSQL, with SQLite fallback when `DATABASE_URL` is absent
- Vercel for hosting

## Requirements

- Python 3.12 or newer
- Node.js and npm

## Local setup

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/MotchiWebsites/juna.git
   cd juna
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the Python and Node.js dependencies:

   ```bash
   python -m pip install -r requirements.txt
   npm ci
   ```

4. Create your local environment file:

   ```bash
   cp .env.example .env
   ```

   Replace `DJANGO_SECRET_KEY` with a local secret. You can generate one with:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Prepare the local database:

   ```bash
   python manage.py migrate
   ```

6. Start Django and the Tailwind watcher together:

   ```bash
   npm run dev
   ```

   The site is available at <http://127.0.0.1:8000/>.

## Common commands

| Command | Purpose |
| --- | --- |
| `npm run dev` | Run Django and watch the Tailwind source |
| `npm run dev:django` | Run only the Django development server |
| `npm run dev:css` | Watch and compile only the Tailwind source |
| `npm run build` | Copy HTMX and create minified production CSS |
| `python manage.py test` | Run the Django test suite |
| `python manage.py check` | Run Django's system checks |
| `python manage.py makemigrations` | Create migrations after model changes |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create a staff administrator |
| `python manage.py collectstatic` | Gather static files for production |
| `python manage.py check --deploy` | Audit production security settings |

## Environment variables

Configuration belongs in environment variables, not committed source files.
Copy `.env.example` to `.env` for local development.

| Variable | Required | Description |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Yes | Private Django signing key |
| `DJANGO_DEBUG` | No | Enables debug mode; defaults to `False` |
| `DJANGO_ALLOWED_HOSTS` | Production | Comma-separated hostnames accepted by Django |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Production | Comma-separated trusted origins, including scheme |
| `DJANGO_TIME_ZONE` | No | Application time zone; defaults to `America/Toronto` |
| `DJANGO_SECURE_HSTS_SECONDS` | No | Production HSTS lifetime; defaults to a cautious 3600 seconds |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | No | Extend HSTS to subdomains only after verifying all use HTTPS |
| `DJANGO_SECURE_HSTS_PRELOAD` | No | Opt into browser preload signaling only after meeting preload requirements |
| `DATABASE_URL` | Production | Neon PostgreSQL connection string; omit it for SQLite |
| `SITE_URL` | Production | Public origin used in canonical and social metadata |

Never commit `.env`, credentials, production database files, or generated
secrets.

## Project structure

```text
.
├── config/                 # Project settings and root URL configuration
├── docs/                   # Architecture and collaboration documentation
├── static/
│   ├── src/app.css         # Tailwind source and project styles
│   ├── js/                 # Browser JavaScript
│   ├── images/
│   │   ├── about/          # Team portraits
│   │   ├── works/          # Portfolio imagery
│   │   └── social/         # Open Graph and X previews
│   ├── icons/              # Decorative and navigation icons
│   ├── css/                # Generated CSS; do not edit directly
│   └── vendor/             # Generated third-party browser assets
├── templates/base.html     # Shared document shell
├── website/                # Main Django application
│   ├── content/            # Immutable homepage content and layout data
│   ├── forms/              # Contact and staff workflow forms
│   ├── models/             # Persistent application models
│   ├── tests/              # Tests organized by feature
│   ├── templates/website/  # Homepage and reusable template partials
│   │   └── partials/
│   │       ├── components/ # Reusable about, navigation, service, and work UI
│   │       └── sections/   # Homepage section composition
│   ├── templatetags/       # Custom Django template tags
│   ├── staff_urls.py       # Staff contact-request routes
│   ├── staff_views.py      # Permission-protected staff workflows
│   ├── urls.py             # Application routes
│   └── views.py            # Request handlers
├── manage.py
├── package.json            # Frontend scripts and dependencies
└── requirements.txt        # Python dependencies
```

See [Architecture](docs/architecture.md) for request flow, ownership
boundaries, static assets, templates, and deployment details.

## Development conventions

- Keep project-wide configuration in `config/` and site behavior in
  `website/`.
- Keep views thin. Put reusable data access and domain behavior in focused
  modules rather than templates or settings.
- Name every URL and reverse it by name instead of hard-coding internal paths.
- Keep `home.html` focused on metadata and composition. Build homepage
  sections in `partials/sections/`, reusable markup in `partials/components/`,
  and authored homepage content in `website/content/`.
- Control the responsive gap between homepage sections on the wrapper in
  `home.html`; keep section-internal spacing inside each section component.
- Define homepage heading copy and emphasis segments in
  `website/content/headings.py`. The shared heading component owns semantic
  levels and responsive typography.
- Edit `static/src/app.css`; never hand-edit generated `static/css/app.css`.
- Prefer Tailwind utilities in templates. Shared authored utilities such as
  `text-emphasis` and `font-regular` live in `static/src/app.css`.
- Give every image meaningful alternative text or an intentional empty `alt`,
  plus its source `width` and `height` to prevent layout shift.
- Add `data-reveal` to content that should enter once as it reaches the
  viewport. The shared behavior lives in `static/js/scroll-reveal.js`, remains
  visible without JavaScript, and respects reduced-motion preferences. Place
  it on the content itself rather than a full-height layout container so the
  reveal begins when that content becomes visible.
- Put secrets and environment-specific values in environment variables.
- Create and commit migrations with every model change.
- Add or update tests for behavior changes.
- Update this README and relevant files in `docs/` whenever setup,
  architecture, commands, configuration, or deployment behavior changes.

The complete workflow is in [Contributing](CONTRIBUTING.md).

## Routes

| Route | URL name | Purpose |
| --- | --- | --- |
| `/` | `website:home` | Single-page website and section navigation |
| `/robots.txt` | `website:robots_txt` | Crawler rules and sitemap discovery |
| `/sitemap.xml` | `website:sitemap_xml` | Public canonical URL sitemap |
| `/staff/` | `website:staff_portal` | Memorable staff shortcut; login required |
| `/admin-portal/contact-requests/` | `website_staff:contact_request_list` | Responsive contact-request workspace |
| `/admin-portal/` | `admin:index` | Django administration and custom staff login |

Create an administrator with `python manage.py createsuperuser`, then use
`/staff/`. Authorized staff also see a **Staff portal** link in the public
navigation while signed in. Contact-request access is controlled by Django's
`view_contactsubmission` and `change_contactsubmission` permissions.

## Deployment

`vercel.json` defines the production build:

```bash
npm ci --include=dev
npm run build
python manage.py collectstatic --noinput
```

Configure all production environment variables in the hosting environment.
Vercel preview hostnames and CSRF origins are handled by `config/settings.py`.
Before a production release, run:

```bash
python manage.py check --deploy
python manage.py test
npm run build
python manage.py collectstatic --noinput
python manage.py migrate --check
```

Verify that `DJANGO_DEBUG=False`, `SITE_URL` uses the final HTTPS origin, hosts
and CSRF origins are exact, and Neon backups are enabled. Production enables
secure cookies, HTTPS redirects, and a one-hour HSTS policy by default. Increase
HSTS gradually only after HTTPS is confirmed across every production host.
Configure platform rate limits for `/contact/submit/` and
`/admin-portal/login/`; Django authentication protects credentials and
permissions but does not provide brute-force throttling by itself.

## Documentation

- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)

Documentation is part of the change: if a pull request changes how the project
is installed, configured, structured, tested, or deployed, it must update the
corresponding documentation in the same pull request.

## License

This project is licensed under the GNU General Public License v3.0. See
[LICENSE](LICENSE).
