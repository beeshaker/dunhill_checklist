from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Site,
    UserProfile,
    UserSite,
    ChecklistSubmission,
    ChecklistResponse,
    DailyQuestion,
    DailyQuestionAssignment,
    QuestionOverride,
)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "portfolio_type")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")


@admin.register(UserSite)
class UserSiteAdmin(admin.ModelAdmin):
    list_display = ("user", "site")


@admin.register(ChecklistSubmission)
class ChecklistSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "site",
        "checklist_type",
        "inspection_date",
        "submitted_at",
        "view_report_link",
        "download_pdf_link",
    )
    list_filter = ("checklist_type", "inspection_date", "site")
    search_fields = ("user__username", "site__name")

    def view_report_link(self, obj):
        url = reverse("checklist_submission_report", args=[obj.id])
        return format_html('<a href="{}" target="_blank">View Report</a>', url)
    view_report_link.short_description = "View Report"

    def download_pdf_link(self, obj):
        url = reverse("checklist_submission_report_pdf", args=[obj.id])
        return format_html('<a href="{}" target="_blank">Download PDF</a>', url)
    download_pdf_link.short_description = "PDF"


@admin.register(ChecklistResponse)
class ChecklistResponseAdmin(admin.ModelAdmin):
    list_display = ("submission", "item_id", "item_status", "escalation_level")
    list_filter = ("item_status", "escalation_level")
    search_fields = ("item_id", "control_item", "module")


@admin.register(DailyQuestion)
class DailyQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "short_question", "correct_option", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("question_text",)

    def short_question(self, obj):
        return obj.question_text[:80]
    short_question.short_description = "Question"


@admin.register(DailyQuestionAssignment)
class DailyQuestionAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "question",
        "assignment_date",
        "started_at",
        "answered_at",
        "is_correct",
        "score",
        "timed_out",
    )
    list_filter = ("assignment_date", "is_correct", "timed_out")
    search_fields = ("user__username", "question__question_text")
    readonly_fields = (
        "user",
        "question",
        "assignment_date",
        "assigned_at",
        "started_at",
        "selected_option",
        "is_correct",
        "answered_at",
        "score",
        "timed_out",
    )

    def has_add_permission(self, request):
        return False


@admin.register(QuestionOverride)
class QuestionOverrideAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "question",
        "forced_by",
        "created_at",
        "started_at",
        "answered_at",
        "is_correct",
        "score",
        "timed_out",
        "is_active",
    )
    list_filter = ("is_active", "is_correct", "timed_out", "created_at")
    search_fields = ("user__username", "question__question_text", "forced_by__username")

    def get_fields(self, request, obj=None):
        if obj is None:
            return (
                "user",
                "question",
                "forced_by",
                "is_active",
                "note",
            )
        return (
            "user",
            "question",
            "forced_by",
            "is_active",
            "note",
            "created_at",
            "started_at",
            "selected_option",
            "is_correct",
            "answered_at",
            "score",
            "timed_out",
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return (
            "user",
            "question",
            "forced_by",
            "created_at",
            "started_at",
            "selected_option",
            "is_correct",
            "answered_at",
            "score",
            "timed_out",
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.started_at = None
            obj.answered_at = None
            obj.selected_option = ""
            obj.is_correct = None
            obj.score = 0
            obj.timed_out = False
        super().save_model(request, obj, form, change)