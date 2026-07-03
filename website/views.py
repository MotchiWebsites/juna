from django.shortcuts import render

from .content.headings import HOMEPAGE_HEADINGS
from .content.services import SERVICES
from .content.team import TEAM_MEMBERS
from .content.works import WORK_GRID
from .forms import ContactForm


def home(request):
    contact_form = ContactForm(
        request.POST if request.method == "POST" else None
    )

    return render(
        request,
        "website/home.html",
        {
            "contact_form": contact_form,
            "headings": HOMEPAGE_HEADINGS,
            "services": SERVICES,
            "team_members": TEAM_MEMBERS,
            "work_grid": WORK_GRID,
        },
    )
