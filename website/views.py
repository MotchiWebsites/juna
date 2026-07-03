from django.shortcuts import render

from .content.headings import HOMEPAGE_HEADINGS
from .content.services import SERVICES
from .content.team import TEAM_MEMBERS
from .content.works import WORK_GRID


def home(request):
    return render(
        request,
        "website/home.html",
        {
            "headings": HOMEPAGE_HEADINGS,
            "services": SERVICES,
            "team_members": TEAM_MEMBERS,
            "work_grid": WORK_GRID,
        },
    )
