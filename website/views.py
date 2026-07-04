from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .content.headings import HOMEPAGE_HEADINGS
from .content.services import SERVICES
from .content.team import TEAM_MEMBERS
from .content.works import WORK_GRID
from .context_processors import get_site_url
from .forms import ContactForm


def _home_context(contact_form=None):
    return {
        "contact_form": (
            contact_form if contact_form is not None else ContactForm()
        ),
        "headings": HOMEPAGE_HEADINGS,
        "services": SERVICES,
        "team_members": TEAM_MEMBERS,
        "work_grid": WORK_GRID,
    }


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


@require_POST
def submit_contact(request):
    contact_form = ContactForm(request.POST)

    if not contact_form.is_valid():
        if _is_htmx(request):
            return render(
                request,
                "website/partials/components/contact/form.html",
                {"contact_form": contact_form},
            )

        return render(
            request,
            "website/home.html",
            _home_context(contact_form),
        )

    contact_form.save()
    messages.success(request, "Thanks! We received your project details.")

    if _is_htmx(request):
        return render(
            request,
            "website/partials/components/contact/submission_response.html",
            {"contact_form": ContactForm()},
        )

    return redirect(f"{reverse('website:home')}#contact")


@require_GET
def home(request):
    return render(
        request,
        "website/home.html",
        _home_context(),
    )


@require_GET
def robots_txt(request):
    return render(
        request,
        "website/seo/robots.txt",
        {"site_url": get_site_url(request)},
        content_type="text/plain",
    )


@require_GET
def sitemap_xml(request):
    return render(
        request,
        "website/seo/sitemap.xml",
        {"site_url": get_site_url(request)},
        content_type="application/xml",
    )
