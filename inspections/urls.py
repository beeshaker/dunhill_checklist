from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("checklists/", views.select_checklist, name="select_checklist"),
    path("checklists/<str:ctype>/sites/", views.select_site, name="select_site"),
    path("checklists/<str:ctype>/site/<int:site_id>/", views.checklist_form, name="checklist_form"),
    path("success/<int:submission_id>/", views.success_page, name="success_page"),

    path("submissions/", views.checklist_submissions, name="checklist_submissions"),
    path("submissions/<int:submission_id>/report/", views.checklist_submission_report, name="checklist_submission_report"),
    path("submissions/<int:submission_id>/report/pdf/", views.checklist_submission_report_pdf, name="checklist_submission_report_pdf"),

    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("admin-panel/create-site/", views.create_site, name="create_site"),
    path("admin-panel/create-user/", views.create_user, name="create_user"),
    path("admin-panel/assign-site/", views.assign_site, name="assign_site"),

    path("admin-panel/checklist-items/", views.checklist_item_builder, name="checklist_item_builder"),
    path("admin-panel/checklist-items/<int:item_id>/toggle/", views.toggle_checklist_item_status, name="toggle_checklist_item_status"),

    path("daily-question/intro/", views.daily_question_intro, name="daily_question_intro"),
    path("daily-question/", views.daily_question, name="daily_question"),
    path("admin-panel/question-admin/", views.question_admin, name="question_admin"),
]