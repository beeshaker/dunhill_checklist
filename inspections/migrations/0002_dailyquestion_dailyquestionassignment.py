from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("inspections", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("site_supervisor", "Site Supervisor"), ("asset_manager", "Asset Manager / Portfolio Head")], max_length=50)),
                ("question_text", models.TextField()),
                ("option_a", models.CharField(max_length=255)),
                ("option_b", models.CharField(max_length=255)),
                ("option_c", models.CharField(max_length=255)),
                ("option_d", models.CharField(max_length=255)),
                ("correct_option", models.CharField(choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("explanation", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["role", "id"]},
        ),
        migrations.CreateModel(
            name="DailyQuestionAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("assignment_date", models.DateField(default=django.utils.timezone.localdate)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("selected_option", models.CharField(blank=True, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("is_correct", models.BooleanField(blank=True, null=True)),
                ("answered_at", models.DateTimeField(blank=True, null=True)),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("timed_out", models.BooleanField(default=False)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="inspections.dailyquestion")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="daily_question_assignments", to="auth.user")),
            ],
            options={"ordering": ["-assignment_date", "-assigned_at"], "unique_together": {("user", "assignment_date")}},
        ),
    ]
