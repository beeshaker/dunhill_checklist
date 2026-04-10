from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("daily-question/intro/", views.daily_question_intro, name="daily_question_intro"),
    path("daily-question/", views.daily_question, name="daily_question"),

    path("select-checklist/", views.select_checklist, name="select_checklist"),
    path("select-site/<str:ctype>/", views.select_site, name="select_site"),
    path("checklist/<str:ctype>/<int:site_id>/", views.checklist_form, name="checklist_form"),
    path("success/<int:submission_id>/", views.success_page, name="success_page"),

    path("submissions/", views.checklist_submissions, name="checklist_submissions"),
    path("submissions/<int:submission_id>/report/", views.checklist_submission_report, name="checklist_submission_report"),
    path("submissions/<int:submission_id>/report/pdf/", views.checklist_submission_report_pdf, name="checklist_submission_report_pdf"),

    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("admin-panel/create-site/", views.create_site, name="create_site"),
    path("admin-panel/create-user/", views.create_user, name="create_user"),
    path("admin-panel/assign-site/", views.assign_site, name="assign_site"),
    path("admin-panel/questions/", views.question_admin, name="question_admin"),
]