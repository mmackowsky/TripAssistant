from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


from .views import (ResetPasswordView, activate, login_request, logout_request,
                    signup, profile)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path('activate/<uid64>/<token>',
         activate, name='activate'),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
    path('profile/', profile, name="profile"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uid64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('social-auth/', include('social_django.urls', namespace="social")),
]
