from django.contrib import admin
from django.urls import path, include
from .views import signup, activate, login_request, logout_request


urlpatterns = [
    path("signup/", signup, name="signup"),
    path('activate/<uid64>/<token>',
         activate, name='activate'),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
    # path('social-auth/', include('social_django.urls', namespace="social")),
]
