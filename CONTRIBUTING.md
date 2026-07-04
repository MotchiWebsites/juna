# Contributing to Juna

This guide keeps changes predictable, reviewable, and easy for the next person
to continue.

## Before making a change

1. Follow the setup in the [README](README.md).
2. Create a focused branch from the current shared branch.
3. Check the existing URL, view, template, test, and asset patterns before
   adding a new one.
4. Keep unrelated cleanup out of the change unless it is required for safety
   or correctness.

## Where changes belong

- Project configuration, middleware, and root routing: `config/`
- Site routes and request handling: `website/urls.py` and `website/views.py`
- Authored homepage content: focused modules inside `website/content/`
- Reusable site behavior: a focused module inside `website/`
- Shared page shell: `templates/base.html`
- Homepage composition: `website/templates/website/home.html`
- Homepage section components:
  `website/templates/website/partials/sections/`
- Reusable template components:
  `website/templates/website/partials/components/`
- Tailwind source and custom styles: `static/src/app.css`
- Small browser interactions: `static/js/`
- Tests: focused modules in `website/tests/`
- Setup and usage guidance: `README.md`
- Architecture guidance: `docs/architecture.md`

## Django conventions

- Keep views focused on HTTP concerns: validate input, call application logic,
  and return a response.
- Use Django forms for user input and validation.
- Use Django's ORM for database access and avoid database work in templates.
- Use named, namespaced URLs and `reverse()` or `{% url %}` for internal links.
- Prefer reusable template partials and template tags over duplicated markup.
- Keep authored content in `website/content/` and presentation classes in
  templates. Tailwind cannot reliably discover class names assembled in Python.
- Preserve the shared heading hierarchy: one entry `h1`, followed by section
  `h2` elements and component-level `h3` elements.
- Keep settings environment-driven and fail clearly when required secrets are
  missing.
- Make schema changes through migrations. Review generated migrations before
  committing them.
- Keep admin registration in `admin.py` and application startup configuration
  in `apps.py`.
- Add docstrings where intent is not obvious; do not restate self-explanatory
  code in comments.

## Frontend conventions

- Treat `static/src/app.css` as the CSS source of truth.
- Do not commit `static/css/` or `static/vendor/`; the build recreates them.
- Prefer Tailwind utilities for component styling. Add a shared custom utility
  only when it replaces a repeated semantic pattern, such as `text-emphasis`
  or `font-regular`.
- Adjust spacing between homepage sections on the flex wrapper in `home.html`;
  do not duplicate outer vertical spacing across section templates.
- Keep JavaScript progressive: core content and navigation should remain
  available without it.
- Preserve semantic HTML, keyboard behavior, visible focus states, meaningful
  alternative text, and reduced-motion preferences.
- Optimize images before adding them, use clear durable filenames, and include
  the source `width` and `height` on every image element.
- Group authored images under the appropriate `static/images/about/`,
  `static/images/works/`, or `static/images/social/` folder.
- Apply `data-reveal` to the element that should animate, and use Tailwind
  custom-property utilities for stagger delays instead of inline styles.

## Tests and checks

Run checks proportional to the change. The normal pre-review set is:

```bash
python manage.py check
python manage.py test
npm run build
```

The test command automatically uses isolated in-memory SQLite settings, even
when local development is connected to Neon.

Add regression tests when fixing a bug. For a new page, test its named URL,
status, template output, and important metadata or accessibility contract.

## Documentation policy

Documentation must describe the repository after the proposed change, not the
repository before it.

Update the README or relevant guide when changing:

- setup steps or runtime requirements;
- dependencies or useful commands;
- environment variables or settings;
- routes, application boundaries, or directory structure;
- static asset or template workflows;
- testing, deployment, or operational behavior.

If none apply, the pull request can state that no documentation change is
needed. This explicit check helps the documentation stay trustworthy.

## Pull request checklist

- [ ] The change has one clear purpose.
- [ ] Secrets, local databases, and generated files are not committed.
- [ ] New configuration is environment-driven and documented.
- [ ] Model changes include reviewed migrations.
- [ ] Behavior changes include appropriate tests.
- [ ] Relevant Django checks, tests, and frontend builds pass.
- [ ] Accessibility and responsive behavior were considered.
- [ ] `README.md` and `docs/` reflect the change, or no update is required.

## Commit guidance

Use short, imperative commit subjects that describe the outcome, for example:

```text
Add contact form validation
Document production environment variables
Fix mobile navigation focus handling
```

Keep commits small enough to review and avoid committing local or generated
artifacts.
