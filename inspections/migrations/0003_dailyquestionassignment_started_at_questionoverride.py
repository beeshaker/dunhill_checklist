from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inspections", "0002_dailyquestion_dailyquestionassignment"),
    ]

    operations = [
        migrations.AddField(
            model_name="dailyquestionassignment",
            name="started_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="QuestionOverride",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("selected_option", models.CharField(blank=True, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("is_correct", models.BooleanField(blank=True, null=True)),
                ("answered_at", models.DateTimeField(blank=True, null=True)),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("timed_out", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("note", models.CharField(blank=True, max_length=255)),
                ("forced_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_question_overrides", to="auth.user")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="overrides", to="inspections.dailyquestion")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="question_overrides", to="auth.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
