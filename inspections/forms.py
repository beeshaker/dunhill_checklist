from django import forms
from django.contrib.auth.models import User
from .models import Site, DailyQuestion, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "portfolio_type", "address"]


class UserCreateForm(forms.Form):
    ROLE_CHOICES = [
        ("site_supervisor", "Site Supervisor"),
        ("asset_manager", "Asset Manager"),
        ("portfolio_head", "Portfolio Head"),
        ("admin", "Admin"),
    ]

    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


class AssignSiteForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all().order_by("username"))
    site = forms.ModelChoiceField(queryset=Site.objects.all().order_by("name"))


class DailyQuestionAnswerForm(forms.Form):
    selected_option = forms.ChoiceField(
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        widget=forms.RadioSelect,
    )


class DailyQuestionOverrideForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        help_text="Choose the employee who should be prompted with a question on the next login.",
    )
    question = forms.ModelChoiceField(
        queryset=DailyQuestion.objects.filter(is_active=True).order_by("role", "id"),
        help_text="Choose the exact question to force for testing or retraining.",
    )
    note = forms.CharField(required=False, max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.exclude(is_superuser=True).order_by("username")

    def clean(self):
        cleaned = super().clean()
        user = cleaned.get("user")
        question = cleaned.get("question")
        if not user or not question:
            return cleaned

        profile = getattr(user, "userprofile", None)
        role = profile.role if profile else "site_supervisor"
        allowed_roles = ["asset_manager"] if role in ["asset_manager", "portfolio_head"] else ["site_supervisor"]
        if question.role not in allowed_roles:
            raise forms.ValidationError("This question does not match the selected employee's role.")
        return cleaned


class QuestionResultFilterForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.none(), required=False)
    question = forms.ModelChoiceField(queryset=DailyQuestion.objects.all().order_by("role", "id"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.exclude(is_superuser=True).order_by("username")
