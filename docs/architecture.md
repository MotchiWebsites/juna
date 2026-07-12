# Architecture

This document explains the current application shape and the intended
boundaries for future work.

## Overview

Juna is a conventional server-rendered Django project with one application,
`website`. Django owns routing, page rendering, metadata, and static asset
references. Tailwind generates the stylesheet, vanilla JavaScript enhances
navigation and viewport reveals, and HTMX is available as a locally served
vendor asset.

The project is intentionally small. New layers should be added when real
behavior requires them, not in anticipation of possible complexity.

## Request flow

```text
Browser request
    → config/urls.py
    → website/urls.py or website/staff_urls.py
    → website/views.py or website/staff_views.py
        → website/content/
    → website/templates/website/home.html
        → templates/base.html
        → website/templates/website/partials/sections/
            → website/templates/website/partials/components/
    → HTML response
```

`website.context_processors.site_settings` adds the public site origin and
canonical URL to every template. The base template uses those values for
canonical, Open Graph, and social metadata. `SITE_URL` must be a path-free
HTTPS origin whenever debug mode is disabled.

Search discovery is served from `/robots.txt` and `/sitemap.xml`. The homepage
publishes linked `WebSite` and `Organization` JSON-LD nodes: `WebSite` declares
the preferred search-result site name, while `Organization` describes the
brand behind the site. Both use `SITE_URL` so schema identifiers, canonical
links, crawler files, and social metadata share one public origin. Staff and
admin surfaces are explicitly excluded from indexing. The web manifest
supports browser installation and is separate from search indexing. Document
favicon links use the stable assets under `static/favicon/` so browsers and
search results receive a consistent brand mark.

`website.middleware.SecurityHeadersMiddleware` adds restrictive browser
permissions and applies `X-Robots-Tag: noindex, nofollow` to private routes and
every Vercel preview response. Private responses are also marked `no-store`.
Robots rules intentionally allow crawlers to request those URLs so the HTTP
`noindex` directive can be observed; authentication and authorization, not
robots rules, protect staff data.

## Django project and application boundaries

### `config/`

`config` is the Django project package. It owns:

- environment-backed settings;
- installed applications and middleware;
- root URL inclusion;
- WSGI and ASGI entry points.

Feature behavior should not accumulate here. Put site-specific behavior in the
`website` application.

### `website/`

`website` is the site application. It owns:

- the homepage and contact-submission workflows;
- contact models, forms, and admin registration;
- the permission-protected staff workspace;
- immutable heading, navigation, service, team, and work content;
- template context and custom template tags;
- homepage components and tests.

The view currently renders the single-page site. As features grow, keep it thin
and move reusable domain or query logic into clearly named modules inside
`website/`. Avoid generic `utils.py` modules; name modules after the behavior
they own.

## URL design

The project URL configuration mounts `website.urls` at the root, the custom
contact-request workspace at `/admin-portal/contact-requests/`, and Django
admin at `/admin-portal/`. `/staff/` is a memorable, authenticated redirect to
the workspace. The public homepage content is addressed through section
fragments such as `/#about`.

Links from outside the homepage should combine its URL name with a section
fragment:

```django
{% url "website:home" %}#about
```

Python code should use `reverse("website:home")`. This keeps templates and
application code independent of literal path changes.

## Templates

`templates/base.html` owns the document shell, shared metadata, fonts, static
styles, navigation, footer, and script loading.

`website/templates/website/home.html` extends the base template and owns page
metadata plus section composition. Each homepage section is a focused component
under `website/templates/website/partials/sections/`. Reusable UI is grouped by
feature under `website/templates/website/partials/components/`; navigation
chrome lives under `components/navigation/`.

The wrapper in `home.html` is the single source of responsive spacing between
homepage sections. Individual sections own only their internal layout and
horizontal spacing.

Application-specific templates retain the `website/` namespace to prevent
collisions if more Django apps are added.

Custom template tags live in `website/templatetags/`. Keep them presentation
focused; database access and business rules do not belong in template tags.

## Homepage content

Immutable authored content lives under `website/content/`:

- `headings.py` defines semantic heading levels, shared size variants, and
  ordered plain or emphasized text segments;
- `navigation.py` defines the section navigation;
- `services.py` and `team.py` define reusable card content;
- `works.py` separates portfolio content from the rotating bento layout.

`website.views.home` passes these collections to the homepage. Keep Tailwind
class names in templates rather than content modules so Tailwind can discover
and compile them.

The shared heading component renders one page-entry `h1` and section `h2`
elements. Visual sizing is controlled by its variant rather than by changing
semantic heading levels. Existing section headings should remain aligned with
their section's `aria-labelledby` value.

## Navigation

`website/content/navigation.py` is the source of truth for primary navigation
items.
`website.templatetags.navigation_tags.primary_navigation` exposes that data to
the `components/navigation/navigation_links.html` partial. The homepage
sections and their IDs must stay aligned with each navigation item's
`section_id`.

When changing navigation:

1. Update `PRIMARY_NAVIGATION`.
2. Ensure the matching homepage section exists exactly once.
3. Keep mobile and desktop navigation behavior equivalent.
4. Update the navigation tests.

## Static assets

Source-controlled assets live under `static/`:

- `static/src/app.css` is the Tailwind entry point and custom CSS source.
- `static/js/` contains browser enhancements.
- `static/images/`, `static/icons/`, and `static/favicon/` contain authored
  media.

Authored images are grouped by purpose: team portraits under `images/about/`,
portfolio media under `images/works/`, and platform-specific share previews
under `images/social/open-graph/` and `images/social/x/`.

Templates should use Tailwind utilities directly. Small shared utilities belong
in `static/src/app.css`; currently `text-emphasis` provides the outlined
emphasis shell and `font-regular` provides Arial/system body copy at weight
400.

The following directories are generated and ignored:

- `static/css/` from the Tailwind build;
- `static/vendor/` from dependency-copy scripts;
- `staticfiles/` from Django's `collectstatic`.

Never edit generated files directly. `npm run build` reconstructs the frontend
outputs, and `python manage.py collectstatic` gathers deployable static files.

### Viewport reveals

Elements marked with `data-reveal` are revealed once when they enter the
viewport. `static/js/scroll-reveal.js` observes them, while the transition
styles live in `static/src/app.css`. Apply the attribute to the content being
animated, not a full-height section wrapper; observing a large wrapper can
trigger the reveal before its visible content reaches the viewport.

The behavior is progressive:

- content is visible when JavaScript is unavailable;
- browsers without Intersection Observer reveal everything immediately;
- reduced-motion preferences disable the movement;
- only opacity and transforms animate to avoid layout work.

HTMX remains responsible for server interaction and HTML swaps. Its transition
hooks are appropriate when swapped content needs animation, but ordinary
scroll-triggered reveals stay independent of the request lifecycle.
Vercel Firewall can reject a contact submission before Django runs. The toast
enhancement listens for an HTMX `429` response and presents a local rate-limit
message without replacing the form; successful submissions and application
validation continue to use server-rendered toast markup.

## Data and migrations

The application uses Neon PostgreSQL whenever `DATABASE_URL` is present and
falls back to SQLite at `db.sqlite3` when it is absent. The local `.neon` file
stores the non-secret Neon organization and project context; connection
credentials remain in the ignored `.env` file. `ContactSubmission` persists
public inquiries in `contact_submissions`. Its identity and message fields are
immutable in Django admin; authorized staff update only workflow status in the
custom workspace.

For every model change:

1. Run `python manage.py makemigrations`.
2. Inspect the generated migration.
3. Run `python manage.py migrate`.
4. Add tests for model behavior and constraints.
5. Commit the migration with the model change.

Production database decisions should be documented before introducing
persistent application data.

## Configuration and security

`config/settings.py` reads local variables from `.env` through
`python-dotenv`. Hosting environments should inject variables directly.

Security-sensitive defaults are deliberate:

- `DJANGO_SECRET_KEY` has no source-code fallback.
- Debug mode defaults to off.
- Allowed hosts and trusted CSRF origins are environment-controlled.
- Production redirects to HTTPS and uses secure session and CSRF cookies.
- Production starts with a cautious one-hour HSTS duration.
- Django 6's CSP middleware enforces same-origin resources, per-request nonces
  for inline structured data, and explicit Adobe Fonts origins.
- Browser permissions are disabled unless the application needs them.
- Vercel previews and private application routes are excluded from indexing.
- Staff views use Django admin authentication plus model-level permissions.
- `.env`, local databases, collected static files, and generated frontend
  outputs are ignored by Git.

Do not place secrets, host-specific values, or credentials in tracked settings.
New required variables must be added to `.env.example` and documented in the
README.

## Testing

The Django tests under `website/tests/` cover:

- the single public route and removed legacy paths;
- successful homepage rendering and combined metadata;
- required metadata and parsed structured-data relationships;
- CSP nonces, security headers, preview indexing rules, and safe `HEAD`
  requests;
- navigation targets and active state;
- heading hierarchy and shared heading rendering;
- team, work, and service collection rendering;
- intrinsic image dimensions and viewport reveal hooks;
- favicon behavior;
- absolute canonical and social image URLs;
- contact validation and persistence;
- custom staff authentication and permission boundaries;
- responsive request summaries, filtering, and dedicated details;
- HTMX and non-HTMX status-update paths.

Keep tests behavior-oriented. Test public contracts rather than implementation
details, and add a regression test with every bug fix. `manage.py test`
automatically selects `config.test_settings`, which uses in-memory SQLite and
cannot mutate Neon.

## Deployment

Vercel runs the build command in `vercel.json`:

1. Install locked Node.js dependencies.
2. Run Django system checks and the isolated test suite.
3. Copy the HTMX browser asset and compile minified Tailwind CSS.
4. Run Django `collectstatic`.

Django's WSGI entry point is `config.wsgi.application`. Production must supply
the variables documented in the README. Preview deployments receive Vercel
host and CSRF-origin support from `config/settings.py` and cannot be indexed.
`.python-version` pins Python 3.12 across Vercel and CI. GitHub's quality
workflow independently checks security settings, tests, migrations, and both
asset builds before code reaches production.
When Vercel system environment variables are exposed, Django adds only the
exact deployment, branch, and production hostnames to its host and CSRF trust
lists. A `.vercel.app` wildcard remains as a compatibility fallback.

Any change to the deployment target, database, static file serving, or runtime
entry point must update this document and the README in the same change.
