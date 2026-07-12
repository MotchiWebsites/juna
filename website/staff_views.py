from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe

from .forms import ContactSubmissionStatusForm
from .models import ContactSubmission


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _require_permission(request, permission):
    if not request.user.has_perm(permission):
        raise PermissionDenied


def _filtered_submissions(request):
    submissions = ContactSubmission.objects.all()
    query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "").strip()

    if query:
        submissions = submissions.filter(
            Q(name__icontains=query)
            | Q(organization__icontains=query)
            | Q(email__icontains=query)
            | Q(description__icontains=query)
        )

    if selected_status in ContactSubmission.Status.values:
        submissions = submissions.filter(status=selected_status)
    else:
        selected_status = ""

    return submissions, query, selected_status


def _list_context(request):
    submissions, query, selected_status = _filtered_submissions(request)
    page_obj = Paginator(submissions, 20).get_page(request.GET.get("page"))
    summary = ContactSubmission.objects.aggregate(
        total=Count("id"),
        new=Count(
            "id",
            filter=Q(status=ContactSubmission.Status.NEW),
        ),
        in_progress=Count(
            "id",
            filter=Q(status=ContactSubmission.Status.IN_PROGRESS),
        ),
        resolved=Count(
            "id",
            filter=Q(status=ContactSubmission.Status.RESOLVED),
        ),
    )

    return {
        "page_obj": page_obj,
        "query": query,
        "selected_status": selected_status,
        "status_choices": ContactSubmission.Status.choices,
        "summary": summary,
    }


def _detail_context(submission):
    return {
        "submission": submission,
        "status_form": ContactSubmissionStatusForm(instance=submission),
    }


@require_safe
def staff_portal(request):
    _require_permission(request, "website.view_contactsubmission")
    return redirect("website_staff:contact_request_list")


@require_safe
def contact_request_list(request):
    _require_permission(request, "website.view_contactsubmission")
    context = _list_context(request)

    if _is_htmx(request) and request.headers.get("HX-Target") == "request-list":
        return render(
            request,
            "website/staff/contact_requests/_list.html",
            context,
        )

    return render(
        request,
        "website/staff/contact_requests/list.html",
        context,
    )


@require_safe
def contact_request_detail(request, submission_id):
    _require_permission(request, "website.view_contactsubmission")
    submission = get_object_or_404(ContactSubmission, pk=submission_id)

    return render(
        request,
        "website/staff/contact_requests/detail.html",
        _detail_context(submission),
    )


@require_POST
def update_contact_request_status(request, submission_id):
    _require_permission(request, "website.change_contactsubmission")
    submission = get_object_or_404(ContactSubmission, pk=submission_id)
    status_form = ContactSubmissionStatusForm(
        request.POST,
        instance=submission,
    )

    if status_form.is_valid():
        submission = status_form.save()
        messages.success(
            request,
            f"Request from {submission.name} was updated.",
        )
    else:
        messages.error(request, "Choose a valid request status.")

    if _is_htmx(request):
        if request.POST.get("presentation") == "inline":
            control_id = request.POST.get("control_id")
            if control_id not in {"table", "card"}:
                control_id = "table"
            response = render(
                request,
                "website/staff/contact_requests/_inline_status_response.html",
                {
                    "submission": submission,
                    "status_choices": ContactSubmission.Status.choices,
                    "can_change": True,
                    "control_id": control_id,
                },
            )
            response["HX-Trigger"] = "contactStatusChanged"
            return response

        response = render(
            request,
            "website/staff/contact_requests/_detail_response.html",
            _detail_context(submission),
        )
        response["HX-Trigger"] = "contactStatusChanged"
        return response

    return redirect(
        reverse(
            "website_staff:contact_request_detail",
            args=(submission.pk,),
        )
    )
