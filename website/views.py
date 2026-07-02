from django.shortcuts import render

from .content.team import TEAM_MEMBERS
from .content.works import WORK_GRID


def home(request):
    return render(
        request,
        "website/home.html",
        {"team_members": TEAM_MEMBERS, "work_grid": WORK_GRID},
    )
