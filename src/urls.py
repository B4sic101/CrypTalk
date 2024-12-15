from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.loginView, name="login"),
    path("register/", views.registerView, name="register"),

    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"), # Password reset submition page

    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"), # renders success email sent message

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), # The link the user receives

    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"), # Succesful password reset
]
