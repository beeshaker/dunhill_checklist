import datetime
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static

from weasyprint import HTML

from .forms import (
    LoginForm,
    SiteForm,
    UserCreateForm,
    AssignSiteForm,
    DailyQuestionAnswerForm,
    DailyQuestionOverrideForm,
    QuestionResultFilterForm,
)
from .models import (
    Site,
    UserSite,
    ChecklistSubmission,
    ChecklistResponse,
    UserProfile,
    DailyQuestion,
    DailyQuestionAssignment,
    QuestionOverride,
)
from .checklist_items import DAILY_ITEMS, WEEKLY_ITEMS, MONTHLY_ITEMS


QUESTION_ROLE_MAP = {
    "site_supervisor": "site_supervisor",
    "asset_manager": "asset_manager",
    "portfolio_head": "asset_manager",
}


def get_items(ctype, portfolio):
    source = {
        "daily": DAILY_ITEMS,
        "weekly": WEEKLY_ITEMS,
        "monthly": MONTHLY_ITEMS,
    }
    items = source.get(ctype, [])
    return [
        i for i in items
        if i["portfolio"].lower() == portfolio.lower()
        or (portfolio in ("S&F", "Serviced & Furnished") and i["portfolio"] == "S&F")
    ]


def group_by_module(items):
    grouped = {}
    for item in items:
        grouped.setdefault(item["module"], []).append(item)
    return grouped


def is_admin_user(user):
    if user.is_superuser:
        return True
    profile = getattr(user, "userprofile", None)
    return bool(profile and profile.role == "admin")


def get_sites_for_user(user):
    if is_admin_user(user):
        return Site.objects.all().distinct()
    return Site.objects.filter(usersite__user=user).distinct()


def decode_base64_image(data_string, item_id):
    if not data_string:
        return None

    try:
        header, data = data_string.split(";base64,")
        mime_type = header.split(":", 1)[1]
        ext = mime_type.split("/")[-1]
        image_bytes = base64.b64decode(data)
        return {
            "bytes": image_bytes,
            "mime_type": mime_type,
            "filename": f"{item_id}.{ext}",
        }
    except Exception:
        return None


def get_question_role_for_user(user):
    if is_admin_user(user):
        return None
    profile = getattr(user, "userprofile", None)
    if not profile:
        return "site_supervisor"
    return QUESTION_ROLE_MAP.get(profile.role)


def get_active_override(user):
    if is_admin_user(user):
        return None
    return (
        QuestionOverride.objects
        .filter(user=user, is_active=True)
        .select_related("question", "forced_by")
        .order_by("created_at")
        .first()
    )


def get_or_create_daily_assignment(user):
    question_role = get_question_role_for_user(user)
    if not question_role:
        return None

    today = timezone.localdate()
    existing = DailyQuestionAssignment.objects.filter(
        user=user,
        assignment_date=today
    ).select_related("question").first()

    if existing:
        return existing

    question = DailyQuestion.objects.filter(
        role=question_role,
        is_active=True
    ).order_by("?").first()

    if not question:
        return None

    return DailyQuestionAssignment.objects.create(
        user=user,
        question=question,
        assignment_date=today,
    )


def get_pending_question_session(user):
    override = get_active_override(user)
    if override and not override.is_answered:
        return "override", override

    assignment = get_or_create_daily_assignment(user)
    if assignment and not assignment.is_answered:
        return "daily", assignment

    return None, None


def questionnaire_needed(user):
    session_type, session_obj = get_pending_question_session(user)
    return bool(session_type and session_obj)


def redirect_if_question_pending(request):
    if questionnaire_needed(request.user):
        return redirect("daily_question_intro")
    return None


def finalize_timed_out(session_obj):
    session_obj.timed_out = True
    session_obj.score = 0
    session_obj.is_correct = False
    session_obj.answered_at = timezone.now()
    update_fields = ["timed_out", "score", "is_correct", "answered_at"]

    if isinstance(session_obj, QuestionOverride):
        session_obj.is_active = False
        update_fields.append("is_active")

    session_obj.save(update_fields=update_fields)


def save_answer(session_obj, selected_option):
    is_correct = selected_option == session_obj.question.correct_option
    session_obj.selected_option = selected_option
    session_obj.is_correct = is_correct
    session_obj.score = 1 if is_correct else 0
    session_obj.answered_at = timezone.now()
    update_fields = ["selected_option", "is_correct", "score", "answered_at"]

    if isinstance(session_obj, QuestionOverride):
        session_obj.is_active = False
        update_fields.append("is_active")

    session_obj.save(update_fields=update_fields)


def get_option_text(question, option_code):
    if option_code == "A":
        return question.option_a
    if option_code == "B":
        return question.option_b
    if option_code == "C":
        return question.option_c
    if option_code == "D":
        return question.option_d
    return ""


def build_question_history_for_user(user):
    daily_qs = (
        DailyQuestionAssignment.objects
        .filter(user=user)
        .select_related("question")
        .order_by("-assigned_at")
    )
    override_qs = (
        QuestionOverride.objects
        .filter(user=user)
        .select_related("question", "forced_by")
        .order_by("-created_at")
    )

    history = []

    for item in daily_qs:
        history.append({
            "kind": "Daily",
            "question_id": item.question_id,
            "question": item.question,
            "asked_at": item.assigned_at,
            "status": "Timed out" if item.timed_out else (
                "Correct" if item.is_correct else (
                    "Incorrect" if item.answered_at else "Pending"
                )
            ),
            "score": item.score,
            "selected_option": item.selected_option,
        })

    for item in override_qs:
        history.append({
            "kind": "Override",
            "question_id": item.question_id,
            "question": item.question,
            "asked_at": item.created_at,
            "status": "Timed out" if item.timed_out else (
                "Correct" if item.is_correct else (
                    "Incorrect" if item.answered_at else "Pending"
                )
            ),
            "score": item.score,
            "selected_option": item.selected_option,
        })

    history.sort(key=lambda x: x["asked_at"], reverse=True)
    return history


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        request.session["login_location_text"] = (request.POST.get("login_location_text") or "").strip()
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            if questionnaire_needed(user):
                return redirect("daily_question_intro")
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")

    return render(request, "inspections/login.html", {"form": form})


@login_required
def daily_question_intro(request):
    if is_admin_user(request.user):
        return redirect("dashboard")

    session_type, session_obj = get_pending_question_session(request.user)
    if not session_obj:
        return redirect("dashboard")

    if request.method == "POST":
        if session_obj.started_at is None:
            session_obj.started_at = timezone.now()
            session_obj.save(update_fields=["started_at"])
        return redirect("daily_question")

    return render(request, "inspections/daily_question_intro.html", {
        "session_type": session_type,
        "session_obj": session_obj,
        "is_admin_user": False,
    })


@login_required
def daily_question(request):
    if is_admin_user(request.user):
        return redirect("dashboard")

    session_type, session_obj = get_pending_question_session(request.user)

    if session_obj is None:
        messages.warning(request, "No active question is available right now.")
        return redirect("dashboard")

    if session_obj.is_answered:
        return redirect("dashboard")

    if session_obj.started_at is None:
        return redirect("daily_question_intro")

    if session_obj.seconds_remaining <= 0:
        finalize_timed_out(session_obj)
        return render(request, "inspections/daily_question_result.html", {
            "assignment": session_obj,
            "is_admin_user": False,
            "timed_out": True,
            "session_type": session_type,
            "correct_option_text": get_option_text(session_obj.question, session_obj.question.correct_option),
            "selected_option_text": "",
        })

    form = DailyQuestionAnswerForm(request.POST or None)

    if request.method == "POST":
        if session_obj.seconds_remaining <= 0:
            finalize_timed_out(session_obj)
            return render(request, "inspections/daily_question_result.html", {
                "assignment": session_obj,
                "is_admin_user": False,
                "timed_out": True,
                "session_type": session_type,
                "correct_option_text": get_option_text(session_obj.question, session_obj.question.correct_option),
                "selected_option_text": "",
            })

        if form.is_valid():
            selected = form.cleaned_data["selected_option"]
            save_answer(session_obj, selected)
            return render(request, "inspections/daily_question_result.html", {
                "assignment": session_obj,
                "is_admin_user": False,
                "timed_out": False,
                "session_type": session_type,
                "correct_option_text": get_option_text(session_obj.question, session_obj.question.correct_option),
                "selected_option_text": get_option_text(session_obj.question, selected),
            })

    return render(request, "inspections/daily_question.html", {
        "assignment": session_obj,
        "form": form,
        "time_limit_seconds": session_obj.seconds_remaining,
        "is_admin_user": False,
        "session_type": session_type,
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    pending_redirect = redirect_if_question_pending(request)
    if pending_redirect:
        return pending_redirect

    user_sites = get_sites_for_user(request.user)
    recent = ChecklistSubmission.objects.filter(user=request.user).order_by("-submitted_at")[:8]
    now = timezone.localtime()
    today = timezone.localdate()

    user_submissions = ChecklistSubmission.objects.filter(user=request.user)
    user_question_stats = DailyQuestionAssignment.objects.filter(user=request.user)
    override_stats = QuestionOverride.objects.filter(user=request.user, answered_at__isnull=False)

    total_submissions = user_submissions.count()
    daily_count = user_submissions.filter(checklist_type="daily").count()
    weekly_count = user_submissions.filter(checklist_type="weekly").count()
    monthly_count = user_submissions.filter(checklist_type="monthly").count()

    issue_count = ChecklistResponse.objects.filter(
        submission__user=request.user,
        item_status="Issue"
    ).count()

    escalations_count = ChecklistResponse.objects.filter(
        submission__user=request.user
    ).exclude(escalation_level="").count()

    recent_by_day_qs = (
        user_submissions
        .annotate(day=TruncDate("submitted_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    chart_labels = [r["day"].strftime("%d %b") for r in recent_by_day_qs]
    chart_values = [r["total"] for r in recent_by_day_qs]

    total_scored = (
        (user_question_stats.aggregate(total=Sum("score"))["total"] or 0) +
        (override_stats.aggregate(total=Sum("score"))["total"] or 0)
    )

    total_answered_question_rows = (
        user_question_stats.filter(answered_at__isnull=False).count() +
        override_stats.count()
    )

    accuracy_pct = (total_scored / total_answered_question_rows) if total_answered_question_rows else 0
    total_questions_answered = total_answered_question_rows
    correct_answers = total_scored
    wrong_answers = (
        user_question_stats.filter(answered_at__isnull=False, score=0).count() +
        override_stats.filter(score=0).count()
    )

    question_due_today = questionnaire_needed(request.user)

    daily_lookback_days = 14
    weekly_lookback_weeks = 8

    missed_daily_sites = []
    missed_weekly_sites = []

    for site in user_sites:
        missed_dates = []

        for i in range(1, daily_lookback_days + 1):
            target_date = today - datetime.timedelta(days=i)
            exists = ChecklistSubmission.objects.filter(
                user=request.user,
                site=site,
                checklist_type="daily",
                inspection_date=target_date
            ).exists()

            if not exists:
                missed_dates.append(target_date)

        if missed_dates:
            missed_daily_sites.append({
                "site_name": site.name,
                "portfolio_type": site.portfolio_type,
                "missed_count": len(missed_dates),
                "missed_dates": missed_dates,
            })

    start_of_this_week = today - datetime.timedelta(days=today.weekday())

    for site in user_sites:
        missed_weeks = []

        for i in range(1, weekly_lookback_weeks + 1):
            week_start = start_of_this_week - datetime.timedelta(weeks=i)
            week_end = week_start + datetime.timedelta(days=6)

            exists = ChecklistSubmission.objects.filter(
                user=request.user,
                site=site,
                checklist_type="weekly",
                inspection_date__range=[week_start, week_end]
            ).exists()

            if not exists:
                missed_weeks.append({
                    "week_start": week_start,
                    "week_end": week_end,
                })

        if missed_weeks:
            missed_weekly_sites.append({
                "site_name": site.name,
                "portfolio_type": site.portfolio_type,
                "missed_count": len(missed_weeks),
                "missed_weeks": missed_weeks,
            })

    return render(request, "inspections/dashboard.html", {
        "sites": user_sites,
        "recent": recent,
        "now": now,
        "is_admin_user": is_admin_user(request.user),
        "total_submissions": total_submissions,
        "daily_count": daily_count,
        "weekly_count": weekly_count,
        "monthly_count": monthly_count,
        "issue_count": issue_count,
        "escalations_count": escalations_count,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "missed_daily_sites": missed_daily_sites,
        "missed_weekly_sites": missed_weekly_sites,
        "missed_daily_site_count": len(missed_daily_sites),
        "missed_weekly_site_count": len(missed_weekly_sites),
        "question_accuracy_pct": round(accuracy_pct * 100, 1),
        "total_questions_answered": total_questions_answered,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "question_due_today": question_due_today,
    })


@login_required
def select_checklist(request):
    pending_redirect = redirect_if_question_pending(request)
    if pending_redirect:
        return pending_redirect

    return render(request, "inspections/select_checklist.html", {
        "is_admin_user": is_admin_user(request.user),
    })


@login_required
def select_site(request, ctype):
    pending_redirect = redirect_if_question_pending(request)
    if pending_redirect:
        return pending_redirect

    sites = get_sites_for_user(request.user)
    return render(request, "inspections/select_site.html", {
        "sites": sites,
        "ctype": ctype,
        "is_admin_user": is_admin_user(request.user),
    })


@login_required
def checklist_form(request, ctype, site_id):
    pending_redirect = redirect_if_question_pending(request)
    if pending_redirect:
        return pending_redirect

    site = get_object_or_404(Site, id=site_id)
    allowed_sites = get_sites_for_user(request.user)

    if not allowed_sites.filter(id=site.id).exists():
        messages.error(request, "You do not have access to this site.")
        return redirect("select_site", ctype=ctype)

    items = get_items(ctype, site.portfolio_type)
    grouped_items = group_by_module(items)
    today = datetime.date.today()

    if request.method == "POST":
        inspection_date = request.POST.get("inspection_date") or str(today)
        submit_location_text = (request.POST.get("submit_location_text") or "").strip()
        login_location_text = (request.session.get("login_location_text") or "").strip()

        submission = ChecklistSubmission.objects.create(
            user=request.user,
            site=site,
            checklist_type=ctype,
            inspection_date=inspection_date,
            login_location_text=login_location_text,
            submit_location_text=submit_location_text,
        )

        has_error = False

        for item in items:
            iid = item["id"]
            status = request.POST.get(f"status_{iid}", "Done")
            remarks = request.POST.get(f"remarks_{iid}", "")
            image_data = request.POST.get(f"photo_data_{iid}", "")

            if not image_data:
                messages.error(request, f"{iid}: live camera photo is required.")
                has_error = True

            if status == "Issue" and not remarks.strip():
                messages.error(request, f"{iid}: remarks are required when status is Issue.")
                has_error = True

        if has_error:
            submission.delete()
            return render(request, "inspections/checklist_form.html", {
                "site": site,
                "ctype": ctype,
                "grouped_items": grouped_items,
                "today": today,
                "is_admin_user": is_admin_user(request.user),
            })

        for item in items:
            iid = item["id"]
            status = request.POST.get(f"status_{iid}", "Done")
            manual_val = request.POST.get(f"value_{iid}", "")
            remarks = request.POST.get(f"remarks_{iid}", "")
            image_data = request.POST.get(f"photo_data_{iid}", "")
            escalation = item.get("escalation", "") if status == "Issue" else ""

            image_file = decode_base64_image(image_data, iid)
            if image_file is None:
                continue

            response = ChecklistResponse.objects.create(
                submission=submission,
                item_id=iid,
                control_item=item["control_item"],
                module=item["module"],
                item_status=status,
                manual_value=manual_val,
                remarks=remarks,
                escalation_level=escalation,
                evidence_image_blob=image_file["bytes"],
                evidence_image_mime_type=image_file["mime_type"],
                evidence_image_filename=image_file["filename"],
            )

        return redirect("success_page", submission_id=submission.id)

    return render(request, "inspections/checklist_form.html", {
        "site": site,
        "ctype": ctype,
        "grouped_items": grouped_items,
        "today": today,
        "is_admin_user": is_admin_user(request.user),
    })


@login_required
def success_page(request, submission_id):
    submission = get_object_or_404(ChecklistSubmission, id=submission_id, user=request.user)
    esc_count = submission.responses.exclude(escalation_level="").count()
    return render(request, "inspections/success.html", {
        "submission": submission,
        "esc_count": esc_count,
        "is_admin_user": is_admin_user(request.user),
    })


@login_required
def checklist_submissions(request):
    if is_admin_user(request.user):
        submissions = (
            ChecklistSubmission.objects
            .select_related("user", "site")
            .prefetch_related("responses")
            .order_by("-submitted_at")
        )
    else:
        submissions = (
            ChecklistSubmission.objects
            .filter(user=request.user)
            .select_related("user", "site")
            .prefetch_related("responses")
            .order_by("-submitted_at")
        )

    return render(request, "inspections/checklist_submissions.html", {
        "submissions": submissions,
        "is_admin_user": is_admin_user(request.user),
    })


@login_required
def checklist_submission_report(request, submission_id):
    submission = get_object_or_404(
        ChecklistSubmission.objects.select_related("user", "site").prefetch_related("responses"),
        id=submission_id
    )

    if not is_admin_user(request.user) and submission.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    responses = submission.responses.all().order_by("module", "item_id")
    done_count = responses.filter(item_status="Done").count()
    issue_count = responses.filter(item_status="Issue").count()
    na_count = responses.filter(item_status="N/A").count()
    photo_count = sum(1 for response in responses if response.has_evidence_image)
    logo_url = request.build_absolute_uri(static("inspections/img/dunhill_logo.png"))

    return render(request, "inspections/checklist_submission_report.html", {
        "submission": submission,
        "responses": responses,
        "is_admin_user": is_admin_user(request.user),
        "logo_url": logo_url,
        "generated_at": timezone.localtime(),
        "done_count": done_count,
        "issue_count": issue_count,
        "na_count": na_count,
        "photo_count": photo_count,
    })


@login_required
def checklist_submission_report_pdf(request, submission_id):
    submission = get_object_or_404(
        ChecklistSubmission.objects.select_related("user", "site").prefetch_related("responses"),
        id=submission_id
    )

    if not is_admin_user(request.user) and submission.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    responses = submission.responses.all().order_by("module", "item_id")
    done_count = responses.filter(item_status="Done").count()
    issue_count = responses.filter(item_status="Issue").count()
    na_count = responses.filter(item_status="N/A").count()
    photo_count = sum(1 for response in responses if response.has_evidence_image)
    logo_url = request.build_absolute_uri(static("inspections/img/dunhill_logo.png"))

    html_string = render_to_string(
        "inspections/checklist_submission_report_pdf.html",
        {
            "submission": submission,
            "responses": responses,
            "logo_url": logo_url,
            "generated_at": timezone.localtime(),
            "done_count": done_count,
            "issue_count": issue_count,
            "na_count": na_count,
            "photo_count": photo_count,
        },
        request=request,
    )

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Dunhill_Checklist_Report_{submission.id}.pdf"'
    return response


@login_required
def admin_panel(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    today = timezone.localdate()
    total_questions = DailyQuestion.objects.count()
    total_answers = (
        DailyQuestionAssignment.objects.filter(answered_at__isnull=False).count() +
        QuestionOverride.objects.filter(answered_at__isnull=False).count()
    )
    pending_overrides = QuestionOverride.objects.filter(is_active=True, answered_at__isnull=True).count()
    today_results = DailyQuestionAssignment.objects.filter(assignment_date=today).count()

    return render(request, "inspections/admin_panel.html", {
        "is_admin_user": True,
        "total_questions": total_questions,
        "total_answers": total_answers,
        "pending_overrides": pending_overrides,
        "today_results": today_results,
    })


@login_required
def create_site(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    form = SiteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Site created successfully.")
        return redirect("create_site")

    sites = Site.objects.all().order_by("name")
    return render(request, "inspections/create_site.html", {
        "form": form,
        "sites": sites,
        "is_admin_user": True,
    })


@login_required
def create_user(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    form = UserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
        )
        UserProfile.objects.create(
            user=user,
            role=form.cleaned_data["role"]
        )
        messages.success(request, f"User '{user.username}' created successfully.")
        return redirect("create_user")

    users = User.objects.select_related("userprofile").all().order_by("username")
    return render(request, "inspections/create_user.html", {
        "form": form,
        "users": users,
        "is_admin_user": True,
    })


@login_required
def assign_site(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    form = AssignSiteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        site = form.cleaned_data["site"]
        UserSite.objects.get_or_create(user=user, site=site)
        messages.success(request, f"Assigned {site.name} to {user.username}.")
        return redirect("assign_site")

    assignments = UserSite.objects.select_related("user", "site").all().order_by("user__username", "site__name")
    return render(request, "inspections/assign_site.html", {
        "form": form,
        "assignments": assignments,
        "is_admin_user": True,
    })


@login_required
def question_admin(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    override_form = DailyQuestionOverrideForm(request.POST or None)
    if request.method == "POST" and override_form.is_valid():
        user = override_form.cleaned_data["user"]
        question = override_form.cleaned_data["question"]
        note = override_form.cleaned_data.get("note", "")

        QuestionOverride.objects.filter(user=user, is_active=True).update(is_active=False)

        QuestionOverride.objects.create(
            user=user,
            question=question,
            forced_by=request.user,
            note=note,
        )
        messages.success(request, f"A forced question has been queued for {user.username} on the next login.")
        return redirect("question_admin")

    filter_form = QuestionResultFilterForm(request.GET or None)
    selected_user = None
    selected_question = None

    if filter_form.is_valid():
        selected_user = filter_form.cleaned_data.get("user")
        selected_question = filter_form.cleaned_data.get("question")

    daily_results = DailyQuestionAssignment.objects.select_related("user", "question")
    override_results = QuestionOverride.objects.select_related("user", "question", "forced_by")

    if selected_user:
        daily_results = daily_results.filter(user=selected_user)
        override_results = override_results.filter(user=selected_user)

    if selected_question:
        daily_results = daily_results.filter(question=selected_question)
        override_results = override_results.filter(question=selected_question)

    result_rows = []

    for item in daily_results.order_by("-assigned_at")[:100]:
        result_rows.append({
            "type": "Daily",
            "user": item.user,
            "question": item.question,
            "asked_at": item.assigned_at,
            "status": "Timed out" if item.timed_out else (
                "Correct" if item.is_correct else (
                    "Incorrect" if item.answered_at else "Pending"
                )
            ),
            "selected_option": item.selected_option,
            "score": item.score,
            "forced_by": None,
        })

    for item in override_results.order_by("-created_at")[:100]:
        result_rows.append({
            "type": "Override",
            "user": item.user,
            "question": item.question,
            "asked_at": item.created_at,
            "status": "Timed out" if item.timed_out else (
                "Correct" if item.is_correct else (
                    "Incorrect" if item.answered_at else "Pending"
                )
            ),
            "selected_option": item.selected_option,
            "score": item.score,
            "forced_by": item.forced_by,
        })

    result_rows.sort(key=lambda x: x["asked_at"], reverse=True)
    result_rows = result_rows[:100]

    user_history = []
    if selected_user:
        user_history = build_question_history_for_user(selected_user)[:50]

    employees = (
        User.objects
        .exclude(is_superuser=True)
        .select_related("userprofile")
        .order_by("username")
    )

    employee_rows = []
    today = timezone.localdate()

    for employee in employees:
        today_assignment = DailyQuestionAssignment.objects.filter(
            user=employee,
            assignment_date=today
        ).select_related("question").first()

        active_override = QuestionOverride.objects.filter(
            user=employee,
            is_active=True
        ).select_related("question").first()

        profile = getattr(employee, "userprofile", None)

        employee_rows.append({
            "user": employee,
            "role": profile.get_role_display() if profile else "Site Supervisor",
            "today_status": "Pending" if today_assignment and not today_assignment.is_answered else (
                "Correct" if today_assignment and today_assignment.is_correct else (
                    "Incorrect" if today_assignment and today_assignment.answered_at else (
                        "Timed out" if today_assignment and today_assignment.timed_out else "Not yet served"
                    )
                )
            ),
            "today_question": today_assignment.question if today_assignment else None,
            "active_override": active_override,
        })

    return render(request, "inspections/question_admin.html", {
        "is_admin_user": True,
        "override_form": override_form,
        "filter_form": filter_form,
        "result_rows": result_rows,
        "user_history": user_history,
        "selected_user": selected_user,
        "employee_rows": employee_rows,
    })