from django import forms
from django.contrib.auth.models import User

from .models import Site, DailyQuestion, ChecklistItem, UserProfile
from .checklist_items import DAILY_ITEMS, WEEKLY_ITEMS, MONTHLY_ITEMS


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


def get_all_module_choices():
    built_in_modules = {
        item["module"]
        for item in (DAILY_ITEMS + WEEKLY_ITEMS + MONTHLY_ITEMS)
        if item.get("module")
    }

    custom_modules = set(
        ChecklistItem.objects.exclude(module__isnull=True)
        .exclude(module__exact="")
        .values_list("module", flat=True)
    )

    all_modules = sorted(built_in_modules | custom_modules)

    choices = [(module, module) for module in all_modules]
    choices.append(("__new__", "+ Create New Module"))
    return choices


class ChecklistItemForm(forms.ModelForm):
    module_choice = forms.ChoiceField(
        choices=[],
        required=False,
        label="Module"
    )
    new_module = forms.CharField(
        required=False,
        label="New Module Name"
    )

    class Meta:
        model = ChecklistItem
        fields = [
            "item_id",
            "checklist_type",
            "module_choice",
            "new_module",
            "control_item",
            "applies_to",
            "site_category",
            "site",
            "requires_photo",
            "escalation",
            "display_order",
            "is_active",
        ]
        widgets = {
            "control_item": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["module_choice"].choices = get_all_module_choices()
        self.fields["site"].queryset = Site.objects.all().order_by("name")
        self.fields["site"].required = False
        self.fields["site_category"].required = False

        if self.instance and self.instance.pk and self.instance.module:
            existing_choices = [c[0] for c in self.fields["module_choice"].choices]
            if self.instance.module in existing_choices:
                self.fields["module_choice"].initial = self.instance.module
            else:
                self.fields["module_choice"].choices = (
                    [(self.instance.module, self.instance.module)]
                    + self.fields["module_choice"].choices
                )
                self.fields["module_choice"].initial = self.instance.module

    def clean(self):
        cleaned_data = super().clean()

        applies_to = cleaned_data.get("applies_to")
        site_category = cleaned_data.get("site_category")
        site = cleaned_data.get("site")
        module_choice = cleaned_data.get("module_choice")
        new_module = (cleaned_data.get("new_module") or "").strip()

        if applies_to == "site_category" and not site_category:
            raise forms.ValidationError("Please select a site category.")

        if applies_to == "individual_site" and not site:
            raise forms.ValidationError("Please select a site.")

        if applies_to == "all":
            cleaned_data["site_category"] = ""
            cleaned_data["site"] = None
        elif applies_to == "site_category":
            cleaned_data["site"] = None
        elif applies_to == "individual_site":
            cleaned_data["site_category"] = ""

        if module_choice == "__new__":
            if not new_module:
                raise forms.ValidationError("Please enter a new module name.")
            cleaned_data["module"] = new_module
        else:
            if not module_choice:
                raise forms.ValidationError("Please select a module.")
            cleaned_data["module"] = module_choice

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.module = self.cleaned_data["module"]
        if commit:
            instance.save()
        return instance


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
    user = forms.ModelChoiceField(
        queryset=User.objects.exclude(is_superuser=True).order_by("username"),
        required=False
    )
    question = forms.ModelChoiceField(
        queryset=DailyQuestion.objects.all().order_by("role", "id"),
        required=False
    )