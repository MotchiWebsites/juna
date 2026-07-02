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
- SQLite for local development
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
| `python manage.py collectstatic` | Gather static files for production |

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
│   ├── images/             # Site imagery
│   ├── icons/              # Decorative and navigation icons
│   ├── css/                # Generated CSS; do not edit directly
│   └── vendor/             # Generated third-party browser assets
├── templates/base.html     # Shared document shell
├── website/                # Main Django application
│   ├── templates/website/  # Homepage and reusable template partials
│   │   └── partials/
│   │       └── sections/   # Homepage section components
│   ├── templatetags/       # Custom Django template tags
│   ├── navigation.py       # Shared navigation data
│   ├── team.py             # Immutable team profile content
│   ├── tests.py            # Application tests
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
  sections as focused components in `partials/sections/`.
- Edit `static/src/app.css`; never hand-edit generated `static/css/app.css`.
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
| `/admin-portal/` | `admin:index` | Django administration |

## Deployment

`vercel.json` defines the production build:

```bash
npm ci --include=dev
npm run build
python manage.py collectstatic --noinput
```

Configure all production environment variables in the hosting environment.
Vercel preview hostnames and CSRF origins are handled by `config/settings.py`.
Before a production release, run the Django checks and tests, verify that
`SITE_URL` uses the final HTTPS origin, and confirm that static assets are
served from `STATIC_ROOT`.

## Documentation

- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)

Documentation is part of the change: if a pull request changes how the project
is installed, configured, structured, tested, or deployed, it must update the
corresponding documentation in the same pull request.

## License

This project is licensed under the GNU General Public License v3.0. See
[LICENSE](LICENSE).
