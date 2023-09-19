from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ResetPasswordView,
    activate,
    login_request,
    logout_request,
    profile,
    signup,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup/<uid64>/<token>/activate", activate, name="activate"),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
    path("profile/", profile, name="profile"),
    path("password-reset/", ResetPasswordView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
