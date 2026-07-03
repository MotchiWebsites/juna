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
    → website/urls.py
    → website/views.py
        → website/content/
    → website/templates/website/home.html
        → templates/base.html
        → website/templates/website/partials/sections/
            → website/templates/website/partials/components/
    → HTML response
```

`website.context_processors.site_settings` adds the public site origin and
canonical URL to every template. The base template uses those values for
canonical, Open Graph, and social metadata.

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

`website` is the public site application. It owns:

- the homepage URL and view;
- future models, forms, and admin registration;
- immutable heading, navigation, service, team, and work content;
- template context and custom template tags;
- homepage components and tests.

The view currently renders the single-page site. As features grow, keep it thin
and move reusable domain or query logic into clearly named modules inside
`website/`. Avoid generic `utils.py` modules; name modules after the behavior
they own.

## URL design

The project URL configuration mounts `website.urls` at the root and exposes the
Django admin at `/admin-portal/`. The public website has one named route,
`website:home`; its content is addressed through section fragments such as
`/#about`.

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

## Data and migrations

Local development uses SQLite at `db.sqlite3`, which is ignored by Git. Django's
session, authentication, and admin applications still require migrations even
while the site has no custom models.

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
- `.env`, local databases, collected static files, and generated frontend
  outputs are ignored by Git.

Do not place secrets, host-specific values, or credentials in tracked settings.
New required variables must be added to `.env.example` and documented in the
README.

## Testing

The current Django tests cover:

- the single public route and removed legacy paths;
- successful homepage rendering and combined metadata;
- required metadata;
- navigation targets and active state;
- heading hierarchy and shared heading rendering;
- team, work, and service collection rendering;
- intrinsic image dimensions and viewport reveal hooks;
- favicon behavior;
- absolute canonical and social image URLs.

Keep tests behavior-oriented. Test public contracts rather than implementation
details, and add a regression test with every bug fix.

If the suite becomes difficult to navigate, replace `website/tests.py` with a
`website/tests/` package organized by feature.

## Deployment

Vercel runs the build command in `vercel.json`:

1. Install locked Node.js dependencies.
2. Copy the HTMX browser asset and compile minified Tailwind CSS.
3. Run Django `collectstatic`.

Django's WSGI entry point is `config.wsgi.application`. Production must supply
the variables documented in the README. Preview deployments receive Vercel
host and CSRF-origin support from `config/settings.py`.

Any change to the deployment target, database, static file serving, or runtime
entry point must update this document and the README in the same change.
