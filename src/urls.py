from django.urls import path

from django.contrib.auth import views as authView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.loginView, name="login"),
    path("register/", views.registerView, name="register"),
    path("logout_user/", views.logout_user, name="logout_user"),

    path("reset_password/", authView.PasswordResetView.as_view(template_name="authentication/passwordReset/password_reset.html"), name="reset_password"), # Password reset submition page

    path("reset_password_sent/", authView.PasswordResetDoneView.as_view(template_name="authentication/passwordReset/password_reset_sent.html"), name="password_reset_done"), # renders success email sent message

    path("reset/<uidb64>/<token>/", authView.PasswordResetConfirmView.as_view(template_name="authentication/passwordReset/password_reset_form.html"), name="password_reset_confirm"), # The link the user receives

    path("reset_password_complete/", authView.PasswordResetCompleteView.as_view(template_name="authentication/passwordReset/password_reset_complete.html"), name="password_reset_complete"), # Succesful password reset
]
