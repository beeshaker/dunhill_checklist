from django.db import models
import base64
from django.contrib.auth.models import User
from django.utils import timezone


class Site(models.Model):
    PORTFOLIO_CHOICES = [
        ("Commercial", "Commercial"),
        ("Warehousing", "Warehousing"),
        ("Residential", "Residential"),
        ("S&F", "S&F"),
    ]

    name = models.CharField(max_length=255)
    portfolio_type = models.CharField(max_length=50, choices=PORTFOLIO_CHOICES)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("site_supervisor", "Site Supervisor"),
        ("asset_manager", "Asset Manager"),
        ("portfolio_head", "Portfolio Head"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="site_supervisor")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "site")


class ChecklistSubmission(models.Model):
    CHECKLIST_TYPES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    checklist_type = models.CharField(max_length=20, choices=CHECKLIST_TYPES)
    inspection_date = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    login_location_text = models.CharField(max_length=255, blank=True)
    submit_location_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.site.name} - {self.checklist_type} - {self.inspection_date}"


class ChecklistResponse(models.Model):
    STATUS_CHOICES = [
        ("Done", "Done"),
        ("Issue", "Issue"),
        ("N/A", "N/A"),
    ]

    submission = models.ForeignKey(ChecklistSubmission, on_delete=models.CASCADE, related_name="responses")
    item_id = models.CharField(max_length=50)
    control_item = models.TextField()
    module = models.CharField(max_length=255)
    item_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    manual_value = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    evidence_image = models.ImageField(upload_to="checklist_evidence/", blank=True, null=True)
    evidence_image_blob = models.BinaryField(blank=True, null=True)
    evidence_image_mime_type = models.CharField(max_length=100, blank=True)
    evidence_image_filename = models.CharField(max_length=255, blank=True)
    escalation_level = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.item_id} - {self.item_status}"

    @property
    def has_evidence_image(self):
        return bool(self.evidence_image_blob or self.evidence_image)

    @property
    def evidence_image_data_url(self):
        if self.evidence_image_blob:
            mime_type = self.evidence_image_mime_type or "image/jpeg"
            encoded = base64.b64encode(self.evidence_image_blob).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        if self.evidence_image:
            try:
                return self.evidence_image.url
            except Exception:
                return ""
        return ""


class DailyQuestion(models.Model):
    ROLE_CHOICES = [
        ("site_supervisor", "Site Supervisor"),
        ("asset_manager", "Asset Manager / Portfolio Head"),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])
    explanation = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["role", "id"]

    def __str__(self):
        return f"{self.get_role_display()} - {self.question_text[:70]}"


class DailyQuestionAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_question_assignments")
    question = models.ForeignKey(DailyQuestion, on_delete=models.CASCADE, related_name="assignments")
    assignment_date = models.DateField(default=timezone.localdate)
    assigned_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    selected_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        blank=True,
    )
    is_correct = models.BooleanField(null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    timed_out = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "assignment_date")
        ordering = ["-assignment_date", "-assigned_at"]

    def __str__(self):
        return f"{self.user.username} - {self.assignment_date}"

    @property
    def is_answered(self):
        return self.answered_at is not None or self.timed_out

    @property
    def time_limit_seconds(self):
        return 60

    @property
    def seconds_remaining(self):
        if not self.started_at:
            return self.time_limit_seconds
        elapsed = (timezone.now() - self.started_at).total_seconds()
        return max(0, self.time_limit_seconds - int(elapsed))


class QuestionOverride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_overrides")
    question = models.ForeignKey(DailyQuestion, on_delete=models.CASCADE, related_name="overrides")
    forced_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_question_overrides")
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    selected_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        blank=True,
    )
    is_correct = models.BooleanField(null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    timed_out = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Override - {self.user.username} - {self.question_id}"

    @property
    def is_answered(self):
        return self.answered_at is not None or self.timed_out

    @property
    def time_limit_seconds(self):
        return 60

    @property
    def seconds_remaining(self):
        if not self.started_at:
            return self.time_limit_seconds
        elapsed = (timezone.now() - self.started_at).total_seconds()
        return max(0, self.time_limit_seconds - int(elapsed))